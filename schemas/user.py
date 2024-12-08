from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(..., min_length=6, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

    class Config:
        orm_mode = True  # Enabled to be used in orm 
        extra = "ignore"  


class UserUpdate(BaseModel):
    username: str = Field(None, min_length=6, max_length=50)
    email: EmailStr = Field(None)
    password: str = Field(None, min_length=6)

    class Config:
        orm_mode = True  # Enabled to be used in orm 
        extra = "ignore" 


class UserLogIn(BaseModel):
    username: str = Field(..., min_length=6, max_length=50)
    password: str = Field(..., min_length=6)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    disabled: bool

    class Config:
        from_attributes = True  # Pydantic V2-Äquivalent zu `orm_mode` in V1
