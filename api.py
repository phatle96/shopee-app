from fastapi import FastAPI
from shopee_utils import auth

app = FastAPI()

@app.get("/shop/createShopAuthLink")
def create_shop_auth_link(partner_id: int, partner_key: str, redirect_url: str = "https://corteza-staging.innity.com.my/api/gateway/shopee/auth/callback/"):
    return auth.create_shop_auth_link(partner_id, partner_key, redirect_url)

@app.post("/shop/getTokenShopLevel")
def get_token_shop_level(code: str, partner_id: int, partner_key: str, shop_id: int):
    return auth.get_token_shop_level(code, partner_id, partner_key, shop_id)

@app.post("/shop/getTokenAccountLevel")
def get_token_account_level(code: str, partner_id: int, partner_key: str, main_account_id: int):
    return auth.get_token_account_level(code, partner_id, partner_key, main_account_id)

@app.post("/shop/refreshTokenShopLevel")
def refresh_token_shop_level(shop_id: int, partner_id: int, partner_key: str, refresh_token: str):
    return auth.refresh_token_shop_level(shop_id, partner_id, partner_key, refresh_token)

@app.post("/shop/refreshTokenMerchantLevel")
def refresh_token_merchant_level(main_account_id: int, partner_id: int, partner_key: str, refresh_token: str):
    return auth.refresh_token_merchant_level(main_account_id, partner_id, partner_key, refresh_token)