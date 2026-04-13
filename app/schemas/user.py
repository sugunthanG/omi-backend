from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    role: str  # "User"


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    is_active: bool

    class Config:
        from_attributes = True