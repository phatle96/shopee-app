import time
import hmac
import hashlib
import os
import jwt

SHOPEE_HOST = os.getenv("SHOPEE_HOST")
SHOPEE_PARTNER_ID = int(os.getenv("SHOPEE_PARTNER_ID"))
SHOPEE_PARTNER_KEY = os.getenv("SHOPEE_PARTNER_KEY")

APP_SECRET_KEY = os.getenv("APP_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def encode_url(
    path: int | None = None, shop_id: int | None = None, redirect_url: str = ""
):
    timest = int(time.time())
    tmp_base_string = "%s%s%s" % (SHOPEE_PARTNER_ID, path, timest)
    if shop_id:
        tmp_base_string += str(shop_id)
    base_string = tmp_base_string.encode()
    partner_key = SHOPEE_PARTNER_KEY.encode()
    sign = hmac.new(partner_key, base_string, hashlib.sha256).hexdigest()
    if shop_id:
        url = (
            SHOPEE_HOST
            + path
            + "?partner_id=%s&timestamp=%s&sign=%s&shop_id=%s"
            % (SHOPEE_PARTNER_ID, timest, sign, shop_id)
        )
    elif redirect_url:
        url = (
            SHOPEE_HOST
            + path
            + "?partner_id=%s&timestamp=%s&sign=%s&redirect=%s"
            % (SHOPEE_PARTNER_ID, timest, sign, redirect_url)
        )
    else:
        url = (
            SHOPEE_HOST
            + path
            + "?partner_id=%s&timestamp=%s&sign=%s" % (SHOPEE_PARTNER_ID, timest, sign)
        )
    return url


def jwt_encode(data: dict):
    return jwt.encode(data, APP_SECRET_KEY, algorithm=ALGORITHM)


def jwt_decode(token: str):
    return jwt.decode(jwt=token, key=APP_SECRET_KEY, algorithms=[ALGORITHM])
