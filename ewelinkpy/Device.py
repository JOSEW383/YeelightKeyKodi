import configparser
import os
import requests
import json


current_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_dir, 'credentials.cfg')
config = configparser.ConfigParser()
config.read(config_file_path)
DOMAIN = config['DOMAIN']['domain']


def get_devices(token):
    url = 'https://'+DOMAIN+'/v2/device/thing'

    headers = {
    'Authorization': 'Bearer '+token,
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers)

    device_data = response.json()["data"]
    # print("get_devices: "+json.dumps(device_data))
    return device_data


def get_device_info(token, device_id):
    url = "https://"+DOMAIN+"/v2/device/thing/status?type=1&id="+device_id

    headers = {
    'Authorization': 'Bearer '+token,
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers)

    device_data = response.json()["data"]["params"]
    # print("get_device_status: "+json.dumps(device_data))
    return device_data


def get_device_status(token, device_id):
    device_data = get_device_info(token, device_id)
    return  device_data["switches"][0]["switch"] == "on"


def set_device_status(token, device_id, turn_on):
    status = "on" if turn_on else "off"
    url = "https://"+DOMAIN+"/v2/device/thing/status"

    payload = json.dumps({
    "type": 1,
    "id": device_id,
    "params": {
        "switches": [
        {
            "switch": status,
            "outlet": 0
        }
        ]
    }
    })
    headers = {
    'Authorization': 'Bearer '+token,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.text)

