import json

import requests

from philips_air_purifier import comms


def get_wifi(air_purifier_host):
    session_key = comms.get_key(air_purifier_host)
    wifi_url = comms.get_api_url(air_purifier_host, "0/wifi")
    response = requests.get(wifi_url)
    response.raise_for_status()
    wifi_response = comms.dh_decrypt(response.text, session_key)
    return json.loads(wifi_response)


def put_wifi(air_purifier_host, ssid=None, pwd=None):
    wifi_settings = {}
    if ssid is not None:
        wifi_settings["ssid"] = ssid
    if pwd is not None:
        wifi_settings["password"] = pwd
    session_key = comms.get_key(air_purifier_host)
    wifi_url = comms.get_api_url(air_purifier_host, "0/wifi")
    encrypted_wifi_settings = comms.dh_encrypt(json.dumps(wifi_settings), session_key)
    response = requests.put(wifi_url, data=encrypted_wifi_settings)
    response.raise_for_status()
    wifi_response = comms.dh_decrypt(response.text, session_key)
    return json.loads(wifi_response)
