import hmac
import json
import time
import requests
import hashlib

## Production Environment：https://partner.shopeemobile.com/api/v2/shop/auth_partner
## Sandbox Environment：https://partner.test-stable.shopeemobile.com/api/v2/shop/auth_partner
HOST = "https://partner.test-stable.shopeemobile.com"


def create_shop_auth_link(partner_id: int, partner_key: str, redirect_url: str):
    timest = int(time.time())
    host = f"{HOST}"
    path = "/api/v2/shop/auth_partner"
    redirect_url = f"{redirect_url}"
    partner_id = f"{partner_id}"
    partner_key = f"{partner_key}"
    partner_key_encode = partner_key.encode()
    tmp_base_string = "%s%s%s" % (partner_id, path, timest)
    base_string = tmp_base_string.encode()
    sign = hmac.new(partner_key_encode, base_string, hashlib.sha256).hexdigest()
    ##generate api
    url = host + path + "?partner_id=%s&timestamp=%s&sign=%s&redirect=%s" % (partner_id, timest, sign, redirect_url)
    return {"url": url}


def get_token_shop_level(code, partner_id, tmp_partner_key, shop_id):
    timest = int(time.time())
    host = f"{HOST}"
    path = "/api/v2/auth/token/get"
    body = {"code": code, "shop_id": shop_id, "partner_id": partner_id}
    tmp_base_string = "%s%s%s" % (partner_id, path, timest)
    base_string = tmp_base_string.encode()
    partner_key = tmp_partner_key.encode()
    sign = hmac.new(partner_key, base_string, hashlib.sha256).hexdigest()
    url = host + path + "?partner_id=%s&timestamp=%s&sign=%s" % (partner_id, timest, sign)
    # print(url)
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=body, headers=headers)
    return response.json()

def get_token_account_level(code, partner_id, tmp_partner_key, main_account_id):
    timest = int(time.time())
    host = f"{HOST}"
    path =  "/api/v2/auth/token/get"
    body = {"code": code, "main_account_id": main_account_id, "partner_id": partner_id}
    tmp_base_string = "%s%s%s" % (partner_id, path, timest)
    base_string = tmp_base_string.encode()
    partner_key = tmp_partner_key.encode()
    sign = hmac.new(partner_key, base_string, hashlib.sha256).hexdigest()
    url = host + path + "?partner_id=%s&timestamp=%s&sign=%s" % (partner_id, timest, sign)

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=body, headers=headers)
    return response.json()

def refresh_token_shop_level(shop_id, partner_id, tmp_partner_key, refresh_token):
    timest = int(time.time())
    host = f"{HOST}"
    path = "/api/v2/auth/access_token/get"
    body = {"shop_id": shop_id, "refresh_token": refresh_token,"partner_id":partner_id}
    tmp_base_string = "%s%s%s" % (partner_id, path, timest)
    base_string = tmp_base_string.encode()
    partner_key = tmp_partner_key.encode()
    sign = hmac.new(partner_key, base_string, hashlib.sha256).hexdigest()
    url = host + path + "?partner_id=%s&timestamp=%s&sign=%s" % (partner_id, timest, sign)
    # print(url)
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=body, headers=headers)
    return response.json()


def refresh_token_merchant_level(merchant_id, partner_id, tmp_partner_key, refresh_token):
    timest = int(time.time())
    host = f"{HOST}"
    path = "/api/v2/auth/access_token/get"
    body = {"merchant_id": merchant_id, "refresh_token": refresh_token}
    tmp_base_string = "%s%s%s" % (partner_id, path, timest)
    base_string = tmp_base_string.encode()
    partner_key = tmp_partner_key.encode()
    sign = hmac.new(partner_key, base_string, hashlib.sha256).hexdigest()
    url = host + path + "?partner_id=%s&timestamp=%s&sign=%s" % (partner_id, timest, sign)

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=body, headers=headers)
    return response.json()

   