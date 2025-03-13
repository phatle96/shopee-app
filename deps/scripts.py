import time
import hmac
import hashlib
import os
import jwt

HOST = os.getenv("HOST")
PARTNER_ID = int(os.getenv("PARTNER_ID"))
PARTNER_KEY = os.getenv("PARTNER_KEY")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def encode_url(
    path: int | None = None, shop_id: int | None = None, redirect_url: str = ""
):
    timest = int(time.time())
    tmp_base_string = "%s%s%s" % (PARTNER_ID, path, timest)
    if shop_id:
        tmp_base_string += str(shop_id)
    base_string = tmp_base_string.encode()
    partner_key = PARTNER_KEY.encode()
    sign = hmac.new(partner_key, base_string, hashlib.sha256).hexdigest()
    if shop_id:
        url = (
            HOST
            + path
            + "?partner_id=%s&timestamp=%s&sign=%s&shop_id=%s"
            % (PARTNER_ID, timest, sign, shop_id)
        )
    elif redirect_url:
        url = (
            HOST
            + path
            + "?partner_id=%s&timestamp=%s&sign=%s&redirect=%s"
            % (PARTNER_ID, timest, sign, redirect_url)
        )
    else:
        url = (
            HOST
            + path
            + "?partner_id=%s&timestamp=%s&sign=%s" % (PARTNER_ID, timest, sign)
        )
    return url


def jwt_encode(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def jwt_decode(token: str):
    return jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
