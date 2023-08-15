import datetime
import os
import requests
import json
import configparser
from .Sign import make_sign_authorization_code, make_sign_access_token


current_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_dir, 'credentials.cfg')
config = configparser.ConfigParser()
config.read(config_file_path)
CLIENT_ID = config['APP_CREDENTIALS']['client_id']
CLIENT_SECRET = config['APP_CREDENTIALS']['client_secret']
USER_EMAIL = config['USER_CREDENTIALS']['user_email']
USER_PASSWORD = config['USER_CREDENTIALS']['user_password']
DOMAIN = config['DOMAIN']['domain']
TIMESTAMP = int(datetime.datetime.now().timestamp()).__str__()


def get_authorization_code():
    sign = make_sign_authorization_code(CLIENT_SECRET, CLIENT_ID, TIMESTAMP)
    url = "https://apia.coolkit.cn/v2/user/oauth/code"
    payload = json.dumps({
        "password": USER_PASSWORD,
        "clientId": CLIENT_ID,
        "state": "idapporuser",
        "redirectUrl": "http://localhost:8888",
        "grantType": "authorization_code",
        "email": USER_EMAIL
    })
    headers = {
    'authorization': 'Sign ' + sign,
    'content-type': 'application/json; charset=utf-8',
    'x-ck-appid': CLIENT_ID,
    'x-ck-seq': TIMESTAMP
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    # print("get_authorization_code: "+response.text)
    authorization_code = response.json()["data"]["code"]
    return authorization_code

def get_access_token(authorization_code):
    url = "https://"+DOMAIN+"/v2/user/oauth/token"

    payload = json.dumps({
    "code": authorization_code,
    "redirectUrl": "http://localhost:8888",
    "grantType": "authorization_code"
    })
    sign = make_sign_access_token(CLIENT_SECRET, payload)
    headers = {
    'X-CK-Nonce': 'gJkdACoO',
    'authorization': 'Sign ' + sign,
    'Content-Type': 'application/json',
    'X-CK-Appid': CLIENT_ID
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    # print("get_access_token: "+response.text)
    token = response.json()["data"]["accessToken"]
    return token
