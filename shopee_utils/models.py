from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


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