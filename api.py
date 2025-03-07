from fastapi import FastAPI, Depends
from shopee_utils import auth, models
import os

from typing import Annotated

from sqlmodel import Field, Session, SQLModel, create_engine, select

POSTGRES_URL = os.getenv("POSTGRES_URL")

# Create database connection
engine = create_engine(POSTGRES_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def on_startup():
    SQLModel.metadata.create_all(engine)


# Run FastAPI
app = FastAPI(lifespan=on_startup())


@app.get("/auth/callback")
def auth_callback(
    db: SessionDep,
    code: str | None = None,
    shop_id: int | None = None,
    main_account_id: int | None = None,
):
    return auth.auth_callback(code, shop_id, main_account_id, db)


@app.get("/shop/createShopAuthLink")
def create_shop_auth_link(
    redirect_url: str = "https://corteza.phatle.dev/api/shopee/auth/callback/",
):
    return auth.create_shop_auth_link(redirect_url)


@app.post("/shop/getTokenFromShopee")
def get_token_from_shopee(
    db: SessionDep,
    code: str,
    shop_id: int | None = None,
    main_account_id: int | None = None,
):
    return auth.get_token_from_shopee(code, shop_id, main_account_id)


@app.post("/shop/refreshTokenFromShopee")
def refresh_token_from_shopee(
    db: SessionDep,
    refresh_token: str,
    shop_id: int | None = None,
    merchant_id: int | None = None,
):
    return auth.refresh_token_from_shopee(shop_id, merchant_id, refresh_token)
