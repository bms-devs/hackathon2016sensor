# hackathon2016sensor
Raspberry Pi-based light sensor developed as part of the 2016 BMS hackathon.

Utilizes a BH1750 light sensor in order to detect whether the toilet is occupied or empty. Sensitivity threshold and other low-level parameters (ie. refresh delay) can be customized in _light-sensor.py_.

## Configuration
Use _config.py_ in order to set up the endpoint where statuses will be reported to.

## Running
_python light-sensor.py_
