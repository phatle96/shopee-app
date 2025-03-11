import time
import hmac
import hashlib
import os

HOST = os.getenv("HOST")
PARTNER_ID = int(os.getenv("PARTNER_ID"))
PARTNER_KEY = os.getenv("PARTNER_KEY")


def encode_url(path: int | None = None, shop_id: int | None = None, redirect_url: str = ""):
    timest = int(time.time())
    tmp_base_string = "%s%s%s" % (PARTNER_ID, path, timest)
    if shop_id:
        tmp_base_string += str(shop_id)
    base_string = tmp_base_string.encode()
    partner_key = PARTNER_KEY.encode()
    sign = hmac.new(partner_key, base_string, hashlib.sha256).hexdigest()
    if shop_id:
        url = HOST + path + "?partner_id=%s&timestamp=%s&sign=%s&shop_id=%s" % (PARTNER_ID, timest, sign, shop_id)
    elif redirect_url:
        url = HOST + path + "?partner_id=%s&timestamp=%s&sign=%s&redirect=%s" % (PARTNER_ID, timest, sign, redirect_url)
    else:
        url = HOST + path + "?partner_id=%s&timestamp=%s&sign=%s" % (PARTNER_ID, timest, sign)
    return url
    

