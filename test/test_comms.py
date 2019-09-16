import os
from philips_air_purifier import comms
from test.mock_purifier import MockPurifier


def test_get_key():
    with MockPurifier() as session:
        assert comms.get_key("192.168.1.12") == session.session_key


def test_exchange_keys():
    private_key, public_key = comms.create_dh_keypair()
    session_key = os.urandom(16)

    def mock_server_key_exchanger(client_public_key):
        shared_secret_key = comms.get_shared_secret_key(client_public_key, private_key)
        encrypted_session_key = comms.aes_encrypt(session_key, shared_secret_key)
        return encrypted_session_key, public_key

    client_session_key = comms.exchange_keys(mock_server_key_exchanger)
    assert client_session_key == session_key


def test_get_api_url():
    assert "http://192.168.0.33/di/v1/products/1/air" == comms.get_api_url(
        "192.168.0.33", "1/air"
    )
