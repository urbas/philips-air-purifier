import json
import requests
from philips_air_purifier.comms import dh_decrypt, get_key, get_api_url

_FAN_SPEED_TO_INT = {"s": 0, "1": 1, "2": 2, "3": 3, "t": 4}


def get_status(air_purifier_host):
    status_url = get_api_url(air_purifier_host, "1/air")
    status = dh_decrypt(requests.get(status_url).text, get_key(air_purifier_host))
    return json.loads(status)


def fan_speed_to_int(status):
    return _FAN_SPEED_TO_INT[status["om"]]


def is_on(status):
    return status["pwr"] == "1"


def is_manual_mode(status):
    return status["mode"] == "M"
