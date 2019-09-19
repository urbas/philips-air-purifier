import json
import requests
from philips_air_purifier import comms

_FAN_SPEED_TO_INT = {"s": 0, "1": 1, "2": 2, "3": 3, "t": 4}


def get_status(air_purifier_host):
    status_url = comms.get_api_url(air_purifier_host, "1/air")
    response = requests.get(status_url)
    response.raise_for_status()
    status = comms.dh_decrypt(response.text, comms.get_key(air_purifier_host))
    return json.loads(status)


def put_status(air_purifier_host, status):
    status_url = comms.get_api_url(air_purifier_host, "1/air")
    status = comms.dh_encrypt(json.dumps(status), comms.get_key(air_purifier_host))
    response = requests.put(status_url, data=status)
    response.raise_for_status()
    status = comms.dh_decrypt(response.text, comms.get_key(air_purifier_host))
    return json.loads(status)


def fan_speed_to_int(status):
    return _FAN_SPEED_TO_INT[status["om"]]


def is_on(status):
    return status["pwr"] == "1"


def is_manual_mode(status):
    return status["mode"] == "M"
