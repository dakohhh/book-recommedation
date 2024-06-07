from fastapi import APIRouter,Request
from ..repository import UserRepository
from .schema.user import SignupSchema

router = APIRouter()



@router.signup("/signup")
async def signup(request: Request, signup: SignupSchema):
    user = await UserRepository.create_user(signup)
    return {"message": "Signup"}