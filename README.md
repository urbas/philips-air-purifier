# Philips Air Purifier Client API
Python API for monitoring and controlling Philips air purifiers.

## Installation
```
pip install philips-air-purifier
```

## Usage
Get the status of the air purifier:
```python
from philips_air_purifier.status import get_status
status = get_status(air_purifier_host="192.168.1.12")
```

## Deploying to PyPi
```bash
pip install setuptools wheel
python setup.py sdist bdist_wheel
twine upload dist/*
```
