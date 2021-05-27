"""
This file help to test the PTZ driver functionality.
"""

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

    # control_mode = config['control_mode']

    ###################
    # SET Position
    ###################

    # get position
    ptz_object.get_pose()
    # move
    ptz_object.move_abs(0.0, 0.0, 0.0)
    #ptz_object.get_pose()

    exit()

    # ptz_object.zoom_in_cont(timeout=10, speed=0.01)

    #
    # # print(ptz_object.ptz_configuration_options.Spaces.AbsoluteZoomPositionSpace[0].XRange.Min)
    #
    #
    # # ptz_object.move_rel()
    #
    # ptz_object.get_pose()

    # ######################
    # # SET Camera
    # #######################
    # media = onvif_device.create_media_service()
    # # Get target profile
    # media_profile = media.GetProfiles()[0]
    #
    # imaging = onvif_device.create_imaging_service()
    #
    # # Get PTZ configuration options for getting continuous move range
    # video_sources = media.GetVideoSources()
    # requestGetImaging = imaging.create_type('GetImagingSettings')
    # requestGetImaging.VideoSourceToken = video_sources[0].token
    # # requestGetImaging.ConfigurationToken = media_profile.PTZConfiguration.token
    # imaging_settings = imaging.GetImagingSettings(requestGetImaging)
    # print('settings:')
    # print(imaging_settings)
    #
    # # requestGetOptions = imaging.create_type('GetOptions')
    # # requestGetOptions.VideoSourceToken = video_sources[0].token
    # # # requestGetImaging.ConfigurationToken = media_profile.PTZConfiguration.token
    # # imaging_settings = imaging.GetOptions(requestGetOptions)
    # # print('settings22:')
    # # print(imaging_settings)
    #
    #
    # requestSetImaging = imaging.create_type('SetImagingSettings')
    # # requestSetImaging.VideoSourceToken = video_sources[0].token
    # requestSetImaging.ImagingSettings = imaging_settings
    # requestSetImaging.ImagingSettings.Brightness = 50
    # requestSetImaging.ForcePersistence = True
    # imaging.SetImagingSettings(requestSetImaging)



    ########################
    # SET ZOOM
    ########################

    # Create media service object
    media = ptz_object.media
    # Get target profile
    media_profile = ptz_object.media_profile
    # print('0 ', self.media_profile)

    # Get Status
    request_status = ptz_object.ptz.create_type('GetStatus')
    request_status.ProfileToken = media_profile.token

    # Get PTZ configuration options for getting continuous move range
    request_config = ptz_object.ptz.create_type('GetConfigurationOptions')
    request_config.ConfigurationToken = media_profile.PTZConfiguration.token
    ptz_configuration_options = ptz_object.ptz.GetConfigurationOptions(request_config)

    # Get range of pan and tilt and zoom
    XMAX = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Max
    zoom_max = ptz_configuration_options.Spaces.AbsoluteZoomPositionSpace[0].XRange.Min
    # print(zoom_max)

    # Get PTZ configuration options for getting continuous move range
    request_config1 = ptz_object.ptz.create_type('GetConfigurations')
    request_config1.ConfigurationToken = media_profile.PTZConfiguration.token
    ptz_configuration_options1 = ptz_object.ptz.GetConfigurations()
    # print(ptz_configuration_options1)

    # Get PTZ configuration options for getting continuous move range
    request_config2 = ptz_object.ptz.create_type('GetConfiguration')
    request_config2.ConfigurationToken = media_profile.PTZConfiguration.token
    ptz_configuration_options2 = ptz_object.ptz.GetConfiguration(request_config2.ConfigurationToken)
    # print(ptz_configuration_options2)


    # Get range of pan and tilt and zoom
    # zoom_max = ptz_configuration_options.DefaultAbsoluteZoomPositionSpace.XRange.Min
    # print(zoom_max)

    # Get all video source configurations
    video_source_configuration = ptz_configuration_options1[0]

    # CHANGE CONFIG
    print('****************************************************')
    # video_source_configuration.ZoomLimits.Range.XRange.Min = -1

    # video_source_configuration.DefaultPTZSpeed.Zoom.x = 0.1

    video_source_configuration.DefaultPTZSpeed.PanTilt.x = 0.1

    # video_source_configuration.DefaultPTZSpeed.PanTilt.y = -1

    # print('--->>> ', video_source_configuration.DefaultPTZSpeed.Zoom.x)
    # print('--->>> ', video_source_configuration.DefaultAbsoluteZoomPositionSpace.XRange.Min)

    # video_source_configuration.ForcePersistence = True

    # # Create request type instance
    request_a = ptz_object.ptz.create_type('SetConfiguration')
    # request_a.ConfigurationToken = media_profile.PTZConfiguration.token

    # request_a.ForcePersistence = True
    # request_a.Configuration = video_source_configuration
    request_a.PTZConfiguration = video_source_configuration
    request_a.ForcePersistence = True

    # print('000 ---->', request_a)

    # Set the video source configuration
    # ptz_object.ptz.SetConfiguration({'PTZConfiguration': request_a.Configuration, 'ForcePersistence': True})

    ptz_object.ptz.SetConfiguration(request_a)


    # ptz_object.move_right_cont(2, 0.7)

    ptz_object.move_abs(0.4, 0.0)

    # ptz_object.get_pose()

    #########################
    # CHECK
    #########################
    # # # Get PTZ configuration options for getting continuous move range
    # request_config2 = ptz_object.ptz.create_type('GetConfiguration')
    # request_config2.ConfigurationToken = media_profile.PTZConfiguration.token
    # ptz_configuration_options2 = ptz_object.ptz.GetConfiguration(request_config2.ConfigurationToken)
    #
    # print('111 ---->', ptz_configuration_options2)
    #
    # # Get PTZ configuration options for getting continuous move range
    # request_config1 = ptz_object.ptz.create_type('GetConfigurations')
    # request_config1.ConfigurationToken = media_profile.PTZConfiguration.token
    # ptz_configuration_options1 = ptz_object.ptz.GetConfigurations()
    # print('222 ---->', ptz_configuration_options1)
    #
    # # ptz_object.move_abs(0, 0)
    #
