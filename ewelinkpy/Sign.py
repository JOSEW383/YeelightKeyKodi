# Python
import hashlib
import hmac
import base64

def make_sign(client_secret:str, message:str) -> str:
    return (base64.b64encode(hmac.new(client_secret.encode(), message.encode(), digestmod=hashlib.sha256).digest())).decode()

def make_sign_authorization_code(client_secret:str, client_id:str, timestamp:str) -> str:
    return make_sign(client_secret,client_id+"_"+timestamp)

def make_sign_access_token(client_secret:str, payload:str) -> str:
    return make_sign(client_secret, payload)
