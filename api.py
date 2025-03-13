from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

import os
from typing import Annotated
from sqlmodel import Session, SQLModel, create_engine


from deps import shopee_oauth2, app_oauth2, models, corteza_oauth2, database


# Tags
APP_OAUTH2 = "Login"
SHOPEE_OAUTH2 = "Shopee OAuth2"
CORTEZA_OAUTH = "Corteza OAuth2"

# CORS
origins = [
    "http://localhost:8090",
    "https://corteza.phatle.dev",
]


# Run FastAPI
app = FastAPI(
    lifespan=SQLModel.metadata.create_all(database.engine),  ## Run when API startup
    title="Shopee API",
    description="API for Shopee",
    version="0.0.1",
    openapi_tags=[
        {
            "name": APP_OAUTH2,
            "description": "Login with Corteza client credential",
        },
        {
            "name": SHOPEE_OAUTH2,
            "description": "Get Authorization from Shopee",
        },
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/auth/login", tags=[APP_OAUTH2])
def login(token: str = Depends(app_oauth2.oauth2_scheme)):
    return {"token": token}


@app.post("/token", tags=[APP_OAUTH2])
async def login_for_access_token(
    db: database.SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> models.Token:
    return app_oauth2.login_for_access_token(db, form_data)


@app.get("/users/me", tags=[APP_OAUTH2])
async def read_users_me(
    db: database.SessionDep,
    current_user: Annotated[
        models.UserBase, Depends(app_oauth2.get_current_active_user)
    ],
):
    return current_user


@app.get("/auth/callback", tags=[SHOPEE_OAUTH2])
async def auth_callback(
    db: database.SessionDep,
    token: str,
    code: str | None = None,
    shop_id: int | None = None,
    main_account_id: int | None = None,
):
    return shopee_oauth2.auth_callback(db, token, code, shop_id, main_account_id)


@app.get("/auth/createShopAuthLink", tags=[SHOPEE_OAUTH2])
def create_shop_auth_link(
    redirect_url: str = "https://corteza.phatle.dev/api/shopee/auth/callback/",
    token: str = Depends(app_oauth2.oauth2_scheme),
):
    return shopee_oauth2.create_shop_auth_link(redirect_url, token)


@app.post("/auth/getTokenFromShopee", tags=[SHOPEE_OAUTH2])
def get_token_from_shopee(
    db: database.SessionDep,
    code: str,
    shop_id: int | None = None,
    main_account_id: int | None = None,
    token: str = Depends(app_oauth2.oauth2_scheme),
):
    return shopee_oauth2.get_token_from_shopee(code, shop_id, main_account_id)


@app.post("/auth/refreshTokenFromShopee", tags=[SHOPEE_OAUTH2])
def refresh_token_from_shopee(
    db: database.SessionDep,
    refresh_token: str,
    shop_id: int | None = None,
    merchant_id: int | None = None,
    token: str = Depends(app_oauth2.oauth2_scheme),
):
    return shopee_oauth2.refresh_token_from_shopee(shop_id, merchant_id, refresh_token)

@app.get("/auth/shopee/getToken", tags=[SHOPEE_OAUTH2])
def shopee_get_token(
    db: database.SessionDep, token: str = Depends(app_oauth2.oauth2_scheme)
):
    return shopee_oauth2.get_token(db, token)


@app.post("/auth/corteza/oauth2", tags=[CORTEZA_OAUTH])
def corteza_client_credential(
    db: database.SessionDep,
    client_id: str,
    client_secret: str,
    tokenUrl: str = "https://corteza.phatle.dev/auth/oauth2/token",
    token: str = Depends(app_oauth2.oauth2_scheme),
):
    return corteza_oauth2.save_client_credentials(
        db, token, client_id, client_secret, tokenUrl
    )


@app.get("/auth/corteza/getToken", tags=[CORTEZA_OAUTH])
def corteza_get_token(
    db: database.SessionDep, token: str = Depends(app_oauth2.oauth2_scheme)
):
    return corteza_oauth2.get_token(db, token)
