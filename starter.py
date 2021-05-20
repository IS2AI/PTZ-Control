from onvif import ONVIFCamera
from utils import PTZ

import yaml

if __name__ == '__main__':

    # get the config params
    config = yaml.safe_load(open("config.yml"))
    config_user = yaml.safe_load(open("config_user.yml"))

    # Define the onvif device
    onvif_device = ONVIFCamera(config_user['ip'], 80, config_user['login'], config_user['password'], 'python-onvif-zeep/wsdl/')

    # create the ptz class
    ptz_object = PTZ(onvif_device)

    control_mode = config['control_mode']

    # get position
    ptz_object.get_pose()
