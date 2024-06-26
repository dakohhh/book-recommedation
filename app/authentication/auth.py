import os
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pydantic import ValidationError
from .schema import Token
from exceptions.custom_exception import CredentialsException
from .hashing import checkPassword
from database.schema import Users
from routers.schema.auth import LoginSchema
from ..repository import UserRepository
from utils.exceptions import BadRequestException
from fastapi import Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


load_dotenv()

bearer = HTTPBearer()

SECRET_KEY = str(os.getenv("SECRET_KEY"))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(days=30)


class AuthToken:
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        self.access_token_expire = ACCESS_TOKEN_EXPIRE_MINUTES

    def create_access_token(self, data):
        token = jwt.encode(
            {"user": data, "exp": datetime.now() + self.access_token_expire}, SECRET_KEY
        )

        return token

    def verify_access_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            instance = Token(**payload)

            if instance.get_expiry_time() < datetime.now():
                raise CredentialsException("access token has expired")

            return instance

        except jwt.PyJWTError as e:
            raise CredentialsException(str(e))

        except ValidationError as e:
            raise CredentialsException("invalid access token")


class Auth:
    def __init__(self):
        self.auth_token = AuthToken()

    async def authenticate_user(self, login_input: LoginSchema):
        user = await UsersRepository.get_user_by_email(email=login_input.email)

        if user is None or not checkPassword(login_input.password, user.password):
            raise BadRequestException("incorrect email or password")

        access_token = self.auth_token.create_access_token(str(user.id))

        return access_token

    async def get_current_user(
        self, request: Request, data: HTTPAuthorizationCredentials = Depends(bearer)
    ) -> Users:
        credentials = data.credentials

        access_token_data = self.auth_token.verify_access_token(credentials)

        user = await UsersRepository.get_user_by_id(access_token_data.user)

        return user


auth = Auth()