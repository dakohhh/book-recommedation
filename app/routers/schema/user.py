from pydantic import BaseModel


class SignupSchema(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
