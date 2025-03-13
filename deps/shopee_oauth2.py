from fastapi import Depends

import os
import json
import requests
from sqlmodel import Session, select

from deps import scripts, models, app_oauth2


# Production Environment：https://partner.shopeemobile.com/api/v2/shop/auth_partner
# Sandbox Environment：https://partner.test-stable.shopeemobile.com/api/v2/shop/auth_partner

SHOPEE_PARTNER_ID = int(os.getenv("SHOPEE_PARTNER_ID"))


def create_shop_auth_link(redirect_url: str, token: str):

    path = "/api/v2/shop/auth_partner"
    authorized_user_url = f"{redirect_url}?token={token}"
    url = scripts.encode_url(path=path, redirect_url=authorized_user_url)

    return {"url": url}


def get_token_from_shopee(code, shop_id: str | None, main_account_id: str | None):

    path = "/api/v2/auth/token/get"
    if main_account_id:
        body = {
            "code": code,
            "main_account_id": main_account_id,
            "partner_id": SHOPEE_PARTNER_ID,
        }
    else:
        body = {"code": code, "shop_id": shop_id, "partner_id": SHOPEE_PARTNER_ID}

    print("body", body)
    url = scripts.encode_url(path=path)

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
            "partner_id": SHOPEE_PARTNER_ID,
        }
    else:
        body = {
            "shop_id": shop_id,
            "refresh_token": refresh_token,
            "partner_id": SHOPEE_PARTNER_ID,
        }
    url = scripts.encode_url(path=path)
    print("url: ", url)
    print("body: ", json.dumps(body))
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=body, headers=headers)

    return response.json()


def auth_callback(
    session: Session,
    token: str,
    code: str | None,
    shop_id: int | None,
    main_account_id: int | None,
):

    try:
        payload = scripts.jwt_decode(token)
        user_id = int(payload.get("sub"))

        if user_id:
            if shop_id or main_account_id:
                shop_id = int(shop_id) if shop_id else None
                main_account_id = main_account_id if main_account_id else None

                callback = models.ShopeeCallbackInDB(
                    code=code,
                    shop_id=shop_id,
                    merchant_id=main_account_id,
                    user_id=user_id,
                    token=token,
                )

                db_callback = models.ShopeeCallbackInDB.model_validate(callback)

                session.add(db_callback)
                session.commit()
                response = get_token_from_shopee(
                    code=code,
                    shop_id=shop_id,
                    main_account_id=main_account_id,
                )

                if response["data"]:
                    credential = models.ShopeeCredentialsInDB(
                        merchant_id=main_account_id,
                        shop_id=shop_id,
                        user_id=user_id,
                        token=token,
                        access_token=response["data"]["access_token"],
                        refresh_token=response["data"]["refresh_token"],
                        request_id=response["data"]["request_id"],
                        expire_in=response["data"]["expire_in"],
                    )

                else:
                    credential = models.ShopeeCredentialsInDB(
                        merchant_id=main_account_id,
                        shop_id=shop_id,
                        user_id=user_id,
                        token=token,
                        auth_error=response["error"]["error"],
                        auth_message=response["error"]["message"],
                        request_id=response["error"]["request_id"],
                    )

                valid_credential = models.ShopeeCredentialsInDB.model_validate(
                    credential
                )
                session.add(valid_credential)
                session.commit()
                session.refresh(valid_credential)

                return valid_credential

        else:
            raise app_oauth2.credentials_exception

    except Exception as e:
        raise app_oauth2.credentials_exception


def get_token(session: Session, token: str):

    try:
        payload = scripts.jwt_decode(token)
        user_id = int(payload.get("sub"))

        if user_id:
            credential = session.exec(
                select(models.ShopeeCredentialsInDB).where(
                    models.ShopeeCredentialsInDB.user_id == user_id
                )
            ).first()

            if credential:
                return credential
            else:
                raise app_oauth2.credentials_exception

        else:
            raise app_oauth2.credentials_exception

    except Exception as e:
        raise app_oauth2.credentials_exception
        # raise e