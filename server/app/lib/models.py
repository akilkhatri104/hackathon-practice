from pydantic import BaseModel,EmailStr

class UserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class SigninRequest(BaseModel):
    username: str
    password: str