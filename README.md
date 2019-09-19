# Philips Air Purifier Client API [![Build](https://travis-ci.org/urbas/philips-air-purifier.svg?branch=master)](https://travis-ci.org/urbas/philips-air-purifier) [![pypi](https://badge.fury.io/py/philips-air-purifier.svg)](https://pypi.org/project/philips-air-purifier/)
Python API for monitoring and controlling Philips air purifiers.

## Installation
```
pip install philips-air-purifier
```

## Usage
Get the status of the air purifier:
```python
from philips_air_purifier import status
status.put_status(air_purifier_host="192.168.1.12", status={"pwr": "1"})
current_status = status.get_status(air_purifier_host="192.168.1.12")
```

## Deploying to PyPi
```bash
pip install setuptools wheel
python setup.py sdist bdist_wheel
twine upload dist/*
```
