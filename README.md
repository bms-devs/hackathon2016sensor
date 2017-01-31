# hackathon2016sensor
Raspberry Pi-based light sensor developed as part of the 2016 BMS hackathon.

Utilizes a BH1750 light sensor in order to detect whether the toilet is occupied or empty. Sensitivity threshold and other low-level parameters (ie. refresh delay) can be customized in _light-sensor.py_.

## Configuration
Use _config.py_ in order to set up the endpoint where statuses will be reported to. In general, reporting happens once in 30 secs and every time the occupied status changes, so the delay is kept minimal.

## Running
_python light-sensor.py_

## Setting up as a system service
* Copy Python scripts to _/opt/light-sensor_. The directory should contain three scripts (_bh1750.py_, _light-sensor.py_ and _config.py_)
* Create a _/lib/systemd/system/light-sensor.service_ file with the following content:
```
[Unit]
Description=Light sensor
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python2 /opt/light-sensor/light-sensor.py
WorkingDirectory=/opt/light-sensor

[Install]
WantedBy=multi-user.target
```
* Register and enable the service with following commands:
```
sudo systemctl daemon-reload
sudo systemctl enable light-sensor.service
sudo systemctl start light-sensor.service
```
