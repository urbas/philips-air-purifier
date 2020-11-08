from philips_air_purifier import wifi
from tests import wifi_responses, mock_purifier


def test_get_wifi():
    with mock_purifier.MockPurifier() as session:
        assert wifi_responses.UNCONFIGURED_WIFI == wifi.get_wifi(session.host)


def test_put_status():
    with mock_purifier.MockPurifier() as session:
        wifi.put_wifi(session.host, ssid="foobar", pwd="supersecret")
        assert "foobar" == wifi.get_wifi(session.host)["ssid"]
