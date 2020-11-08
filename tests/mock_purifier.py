import json
import os
from httmock import urlmatch, HTTMock
from philips_air_purifier import comms
from tests import status_responses, wifi_responses

_MOCK_PURIFIER_HOST = "192.168.1.12"


class MockPurifier(HTTMock):
    def __init__(self, status=None, wifi=None):
        self.session_key = os.urandom(16)
        self.private_key, self.public_key = comms.create_dh_keypair()
        self.host = _MOCK_PURIFIER_HOST
        self.status = status or status_responses.OFF_STATUS.copy()
        self.wifi = wifi or wifi_responses.UNCONFIGURED_WIFI.copy()

        super(MockPurifier, self).__init__(
            self._security_api_handler,
            self._wifi_get_handler,
            self._wifi_put_handler,
            self._status_get_handler,
            self._status_put_handler,
        )

    @urlmatch(
        netloc=_MOCK_PURIFIER_HOST, path="/di/v1/products/0/security", method="PUT"
    )
    def _security_api_handler(self, url, request):
        data = json.loads(request.body.decode("ascii"))
        client_public_key = int(data["diffie"], 16)
        self.shared_secret_key = comms.get_shared_secret_key(
            client_public_key, self.private_key
        )
        encrypted_session_key = comms.aes_encrypt(
            self.session_key, self.shared_secret_key
        )
        return json.dumps(
            {
                "key": encrypted_session_key.hex(),
                "hellman": format(self.public_key, "x"),
            }
        )

    @urlmatch(netloc=_MOCK_PURIFIER_HOST, path="/di/v1/products/0/wifi", method="GET")
    def _wifi_get_handler(self, url, request):
        return comms.dh_encrypt(json.dumps(self.wifi), self.session_key)

    @urlmatch(netloc=_MOCK_PURIFIER_HOST, path="/di/v1/products/0/wifi", method="PUT")
    def _wifi_put_handler(self, url, request):
        new_wifi = json.loads(comms.dh_decrypt(request.body, self.session_key))
        self.wifi = wifi_responses.configured_wifi(new_wifi["ssid"])
        return comms.dh_encrypt(json.dumps(self.wifi), self.session_key)

    @urlmatch(netloc=_MOCK_PURIFIER_HOST, path="/di/v1/products/1/air", method="GET")
    def _status_get_handler(self, url, request):
        return comms.dh_encrypt(json.dumps(self.status), self.session_key)

    @urlmatch(netloc=_MOCK_PURIFIER_HOST, path="/di/v1/products/1/air", method="PUT")
    def _status_put_handler(self, url, request):
        new_status = json.loads(comms.dh_decrypt(request.body, self.session_key))
        self.status.update(new_status)
        return comms.dh_encrypt(json.dumps(self.status), self.session_key)

    def __enter__(self):
        return super(MockPurifier, self).__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return super(MockPurifier, self).__exit__(exc_type, exc_val, exc_tb)
