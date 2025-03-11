from sqlmodel import Field, SQLModel

from pydantic import BaseModel


class CredentialBase(SQLModel):
    shopId: int | None
    merchantId: int | None
    accessToken: str | None
    refreshToken: str | None
    authError: str | None
    authMessage: str | None
    expireIn: int | None
    requestId: str | None


class CallBackbBase(SQLModel):
    code: str | None
    shopId: int | None
    merchantId: int | None


class ShopeeCredential(CredentialBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ShopeeCallback(CallBackbBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str
