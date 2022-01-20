# PTZ-Control
Driver for controlling the PTZ with Python script

# Guidelines:

1) Install Python packages listed in **installations.txt**
2) Clone Python API for ONVIF protocol: https://github.com/FalkTannhaeuser/python-onvif-zeep
3) Config file *config_user.yml* containing login, password, and IP address should be copied separately.
4) Folder **data/** containing map of Nur-Sultan city should be copied separately.
5) For moving to target position on a map, run the command: *python move_to_target.py*. Calibration is required after re-installing the PTZ system.
