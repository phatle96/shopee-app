from sqlmodel import Field, SQLModel

from pydantic import BaseModel


class ShopeeCredentialBase(SQLModel):
    shop_id: int | None
    merchant_id: int | None
    access_token: str | None
    refresh_token: str | None
    auth_error: str | None
    auth_message: str | None
    expire_in: int | None
    request_id: str | None
    user_id: int | None
    token: str | None


class CallBackbBase(SQLModel):
    code: str | None
    shop_id: int | None
    merchant_id: int | None
    user_id: int | None
    token: str | None


class ShopeeCredentialsInDB(ShopeeCredentialBase, table=True):
    __tablename__: str = "shopee_credentials"
    id: int | None = Field(default=None, primary_key=True)


class ShopeeCallbackInDB(CallBackbBase, table=True):
    __tablename__: str = "shopee_callback"
    id: int | None = Field(default=None, primary_key=True)


class CortezaCredentialBase(SQLModel):
    client_id: str
    client_secret: str
    user_id: int | None
    token: str | None
    tokenUrl: str | None


class CortezaCredentialsInDB(CortezaCredentialBase, table=True):
    __tablename__: str = "corteza_credentials"
    id: int | None = Field(default=None, primary_key=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserBase(SQLModel):
    username: str = Field(unique=True)
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(UserBase, table=True):
    __tablename__: str = "users"
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
