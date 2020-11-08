# Philips Air Purifier Client API [![Build](https://travis-ci.org/urbas/philips-air-purifier.svg?branch=master)](https://travis-ci.org/urbas/philips-air-purifier) [![pypi](https://badge.fury.io/py/philips-air-purifier.svg)](https://pypi.org/project/philips-air-purifier/)
Python API for monitoring and controlling Philips air purifiers.

Tested with:
- Philips AC3256/60

## Installation
```
pip install philips-air-purifier
```

## Usage
Get and set the status of the air purifier:
```python
from philips_air_purifier import status
status.put_status(air_purifier_host="192.168.1.12", status={"pwr": "1"})
current_status = status.get_status(air_purifier_host="192.168.1.12")
```

Connect your air purifier to your WiFi network:
1. Set your air purifier to "pairing mode" (look online for instructions).
2. Connect your computer to the WiFi network created by the air purifier.
3. Run this:
   ```python
   from philips_air_purifier import wifi
   wifi.put_wifi(air_purifier_host="192.168.1.1", ssid="your wifi's name", pwd="your wifi's password")
   ```
   At this point the air purifier will leave "pairing mode" and connect to your WiFi network.
4. Re-connect to your WiFi network and find the IP address of the air purifier (by inspecting your router).

## TODO before 1.0.0
- session-based API (to avoid the need to repeat DH key exchange for every call--to support more complicated use cases)
- custom HTTP request API (to support features not covered by the functional and session-based API)