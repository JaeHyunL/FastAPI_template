from pydantic import BaseModel, EmailStr


# 유저 속성공유
class UserBase(BaseModel):
    email: EmailStr | None = None
    is_active: bool | None = True
    is_superuser: bool = False
    full_name: str | None = None


# 생성 시 API를 통해 수신할 속성
class UserCreate(UserBase):
    email: EmailStr
    password: str


# 업데이트 시 API를 통해 수신할 속성
class UserUpdate(UserBase):
    password: str | None = None


class UserInDBase(UserBase):
    id: int | None = None

    class Config:
        orm_mode = True


class User(UserInDBase):
    pass


# DB에 저장된 속성을 추가.
class UserInDB(UserInDBase):
    hashed_password: str


class KaKaoTemplate(UserBase):
    access_token: str
    refresh_token: str
