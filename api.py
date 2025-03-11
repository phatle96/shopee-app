from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm

import os
from typing import Annotated
from sqlmodel import Field, Session, SQLModel, create_engine


from deps import shopee_oauth, oauth, models


POSTGRES_URL = os.getenv("POSTGRES_URL")


# Create database connection
engine = create_engine(POSTGRES_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


# Tags
SHOPEE_AUTH = "Shopee Authorization"
CORTEZA_AUTH = "Corteza Authentication"


# Run FastAPI
app = FastAPI(
    lifespan=SQLModel.metadata.create_all(engine),  ## Run when API startup
    title="Shopee API",
    description="API for Shopee",
    version="0.0.1",
    openapi_tags=[
        {
            "name": CORTEZA_AUTH,
            "description": "Login with Corteza client credential",
        },
        {
            "name": SHOPEE_AUTH,
            "description": "Get Authorization from Shopee",
        },
    ],
)


@app.get("/auth/login", tags=[CORTEZA_AUTH])
def login(token: str = Depends(oauth.oauth2_scheme)):
    return {"token": token}


@app.post("/token", tags=[CORTEZA_AUTH])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> models.Token:
    return oauth.login_for_access_token(form_data)


@app.get("/users/me", tags=[CORTEZA_AUTH])
async def read_users_me(
    current_user: Annotated[models.User, Depends(oauth.get_current_active_user)],
):
    return current_user


@app.get("/auth/callback", tags=[SHOPEE_AUTH])
async def auth_callback(
    db: SessionDep,
    token: str,
    code: str | None = None,
    shop_id: int | None = None,
    main_account_id: int | None = None,
):
    return shopee_oauth.auth_callback(token, code, shop_id, main_account_id, db)


@app.get("/auth/createShopAuthLink", tags=[SHOPEE_AUTH])
def create_shop_auth_link(
    redirect_url: str = "https://corteza.phatle.dev/api/shopee/auth/callback/",
    token: str = Depends(oauth.oauth2_scheme),
):
    return shopee_oauth.create_shop_auth_link(redirect_url, token)


@app.post("/auth/getTokenFromShopee", tags=[SHOPEE_AUTH])
def get_token_from_shopee(
    db: SessionDep,
    code: str,
    shop_id: int | None = None,
    main_account_id: int | None = None,
    token: str = Depends(oauth.oauth2_scheme),
):
    return shopee_oauth.get_token_from_shopee(code, shop_id, main_account_id)


@app.post("/auth/refreshTokenFromShopee", tags=[SHOPEE_AUTH])
def refresh_token_from_shopee(
    db: SessionDep,
    refresh_token: str,
    shop_id: int | None = None,
    merchant_id: int | None = None,
    token: str = Depends(oauth.oauth2_scheme),
):
    return shopee_oauth.refresh_token_from_shopee(shop_id, merchant_id, refresh_token)
