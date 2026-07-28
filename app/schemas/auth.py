from pydantic import BaseModel, EmailStr, Field, model_validator


class RegisterIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6)
    confirm_password: str

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("password and confirm_password do not match")
        return self


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True
