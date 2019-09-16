from philips_air_purifier import status
from test import status_responses, mock_purifier


def test_get_status():
    with mock_purifier.MockPurifier(status=status_responses.SLEEP_STATUS) as session:
        assert status_responses.SLEEP_STATUS == status.get_status(session.host)


def test_fan_speed_to_int():
    assert 0 == status.fan_speed_to_int(status_responses.SLEEP_STATUS)
    assert 1 == status.fan_speed_to_int(status_responses.SPEED_1_STATUS)
    assert 2 == status.fan_speed_to_int(status_responses.SPEED_2_STATUS)
    assert 3 == status.fan_speed_to_int(status_responses.SPEED_3_STATUS)
    assert 4 == status.fan_speed_to_int(status_responses.TURBO_STATUS)


def test_is_on():
    assert not status.is_on(status_responses.OFF_STATUS)
    assert status.is_on(status_responses.SLEEP_STATUS)
    assert status.is_on(status_responses.TURBO_STATUS)


def test_is_manual_mode():
    assert status.is_manual_mode(status_responses.SLEEP_STATUS)
    assert not status.is_manual_mode(status_responses.ALERGEN_MODE)
