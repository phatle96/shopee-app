import json
import time
import requests
from shopee_utils import scripts, models

import os

from sqlmodel import Session

# Production Environment：https://partner.shopeemobile.com/api/v2/shop/auth_partner
# Sandbox Environment：https://partner.test-stable.shopeemobile.com/api/v2/shop/auth_partner
HOST = os.getenv("HOST")

host = os.getenv("HOST")
partner_id = os.getenv("PARTNER_ID")
tmp_partner_key = os.getenv("PARTNER_KEY")


def create_shop_auth_link(redirect_url: str):

    path = "/api/v2/shop/auth_partner"
    url = scripts.encode(path=path, redirect_url=redirect_url)

    return {"url": url}


def get_token_from_shopee(code, shop_id: str | None, main_account_id: str | None):

    path = "/api/v2/auth/token/get"
    if main_account_id:
        body = {
            "code": code,
            "main_account_id": main_account_id,
            "partner_id": int(partner_id),
        }
    else:
        body = {"code": code, "shop_id": shop_id, "partner_id": int(partner_id)}

    print("body", body)
    url = scripts.encode(path=path)

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=body, headers=headers)
    if response.status_code == 200:
        return {"error": "", "data": response.json()}
    else:
        return {"error": response.json(), "data": ""}


def refresh_token_from_shopee(
    shop_id: int | None, merchant_id: int | None, refresh_token: str, session: Session
):

    path = "/api/v2/auth/access_token/get"
    if merchant_id:
        body = {
            "merchant_id": merchant_id,
            "refresh_token": refresh_token,
            "partner_id": int(partner_id),
        }
    else:
        body = {
            "shop_id": shop_id,
            "refresh_token": refresh_token,
            "partner_id": int(partner_id),
        }
    url = scripts.encode(path=path)
    print("url: ", url)
    print("body: ", json.dumps(body))
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=body, headers=headers)

    return response.json()


def auth_callback(
    code: str | None, shop_id: str | None, main_account_id: str | None, session: Session
):

    if shop_id or main_account_id:

        shop_id = shop_id if shop_id else None
        main_account_id = main_account_id if main_account_id else None

        callback = models.ShopeeCallback(
            code=code, shopId=shop_id, merchantId=main_account_id
        )

        db_callback = models.ShopeeCallback.model_validate(callback)

        session.add(db_callback)
        session.commit()
        response = get_token_from_shopee(
            code=code,
            shop_id=shop_id,
            main_account_id=main_account_id,
        )

        if response["data"]:
            credential = models.ShopeeCredential(
                merchantId=main_account_id,
                shopId=shop_id,
                accessToken=response["data"]["access_token"],
                refreshToken=response["data"]["refresh_token"],
                requestId=response["data"]["request_id"],
                expireIn=response["data"]["expire_in"]
            )

        else:
            credential = models.ShopeeCredential(
                merchantId=main_account_id,
                shopId=shop_id,
                authError=response["error"]["error"],
                authMessage=response["error"]["message"],
                requestId=response["error"]["request_id"],
            )

        valid_credential = models.ShopeeCredential.model_validate(credential)
        session.add(valid_credential)
        session.commit()
        session.refresh(valid_credential)

        return valid_credential

    else:
        return {"error": "No shop_id or main_account_id provided"}
    
    