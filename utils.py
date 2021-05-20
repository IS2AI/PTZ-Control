from time import sleep
import numpy as np
import yaml
import time


class PTZ:
    """PTZ object and its basic functionality"""

    def __init__(self, onvif_device):
        print('PTZ initialized ...')
        # import params
        self.config = yaml.safe_load(open("config.yml"))
        self.pan_speed = self.config['pan_speed']
        self.tilt_speed = self.config['tilt_speed']
        self.zoom_speed = self.config['zoom_speed']
        self.threshold_speed = self.config['threshold_speed']

        # limit the speed values
        self.pan_speed = np.clip(self.pan_speed, -self.threshold_speed, self.threshold_speed)
        self.tilt_speed = np.clip(self.tilt_speed, -self.threshold_speed, self.threshold_speed)
        self.zoom_speed = np.clip(self.zoom_speed, -self.threshold_speed, self.threshold_speed)

        # Create ptz service object
        self.ptz = onvif_device.create_ptz_service()

        # Create media service object
        self.media = onvif_device.create_media_service()
        # Get target profile
        self.media_profile = self.media.GetProfiles()[0]
        # print('0 ', self.media_profile)

        # Create imaging service object
        self.imaging = onvif_device.create_imaging_service()

        # Get Status
        self.request_status = self.ptz.create_type('GetStatus')
        self.request_status.ProfileToken = self.media_profile.token

        # # Go to Home Position
        self.request_goto_home = self.ptz.create_type('GotoHomePosition')
        self.request_goto_home.ProfileToken = self.media_profile.token
        # self.ptz.GotoHomePosition(self.request_goto_home)

        # ABSOLUTE MOTION
        # create move request for ABSOLUTE motion
        self.move_request_abs = self.ptz.create_type('AbsoluteMove')
        self.move_request_abs.ProfileToken = self.media_profile.token
        if self.move_request_abs.Position is None:
            self.move_request_abs.Position = self.ptz.GetStatus({'ProfileToken': self.media_profile.token}).Position
        # if self.move_request_abs.Speed is None:
        #     self.move_request_abs.Speed = self.ptz.GetStatus({'ProfileToken': self.media_profile.token}).Position

        # # RELATIVE MOTION
        # This is not currently supported in Ulisse.
        # # # create move request for RELATIVE motion
        # self.move_request_rel = self.ptz.create_type('RelativeMove')
        # self.move_request_rel.ProfileToken = self.media_profile.token
        # if self.move_request_rel.Translation is None:
        #     print('self.move_request_rel.Position is None:')
        #     self.move_request_rel.Translation = self.ptz.GetStatus({'ProfileToken': self.media_profile.token}).Position

        # CONTINUOUS MOTION
        # create move request for continuous motion
        self.move_request_cont = self.ptz.create_type('ContinuousMove')
        self.move_request_cont.ProfileToken = self.media_profile.token
        if self.move_request_cont.Velocity is None:
            self.move_request_cont.Velocity = self.ptz.GetStatus({'ProfileToken': self.media_profile.token}).Position

        # Get PTZ configuration options for getting continuous move range
        self.request_config = self.ptz.create_type('GetConfigurationOptions')
        self.request_config.ConfigurationToken = self.media_profile.PTZConfiguration.token
        self.ptz_configuration_options = self.ptz.GetConfigurationOptions(self.request_config)

        # Get range of pan and tilt and zoom
        self.XMAX = self.ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Max
        self.XMIN = self.ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Min
        self.YMAX = self.ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Max
        self.YMIN = self.ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Min
        self.ZMIN = self.ptz_configuration_options.Spaces.ContinuousZoomVelocitySpace[0].XRange.Min
        self.ZMAX = self.ptz_configuration_options.Spaces.ContinuousZoomVelocitySpace[0].XRange.Max

        # print('max: ', self.ZMIN, self.ZMAX)

    # CONTINUOUS
    # basic motions
    def move_left_cont(self, timeout, speed):
        print('move left.. ')
        self.pan_speed = speed
        self.move_request_cont.Velocity.PanTilt.x = -self.XMAX * self.pan_speed
        self.move_request_cont.Velocity.PanTilt.y = 0
        self.move_request_cont.Velocity.Zoom.x = 0
        self.perform_move_cont(self.move_request_cont, timeout)

    def move_right_cont(self, timeout, speed):
        print('move right.. ')
        self.pan_speed = speed
        self.move_request_cont.Velocity.PanTilt.x = self.XMAX * self.pan_speed
        self.move_request_cont.Velocity.PanTilt.y = 0
        self.move_request_cont.Velocity.Zoom.x = 0
        # self.move_request_cont.Timeout = timeout

        self.perform_move_cont(self.move_request_cont, timeout)

    def move_up_cont(self, timeout, speed):
        print('move up.. ')
        self.tilt_speed = speed
        self.move_request_cont.Velocity.PanTilt.x = 0
        self.move_request_cont.Velocity.PanTilt.y = self.YMAX * self.tilt_speed
        self.move_request_cont.Velocity.Zoom.x = 0
        self.perform_move_cont(self.move_request_cont, timeout)

    def move_down_cont(self, timeout, speed):
        print('move down.. ')
        self.tilt_speed = speed
        self.move_request_cont.Velocity.PanTilt.x = 0
        self.move_request_cont.Velocity.PanTilt.y = -self.YMAX * self.tilt_speed
        self.move_request_cont.Velocity.Zoom.x = 0
        self.perform_move_cont(self.move_request_cont, timeout)

    # zoom
    def zoom_in_cont(self, timeout, speed):
        print('zoom in.. ')
        self.zoom_speed = speed
        self.move_request_cont.Velocity.PanTilt.x = 0
        self.move_request_cont.Velocity.PanTilt.y = 0
        self.move_request_cont.Velocity.Zoom.x = self.ZMAX * self.zoom_speed
        # self.move_request_cont.Timeout = timeout

        self.perform_move_cont(self.move_request_cont, timeout)

    def zoom_out_cont(self, timeout, speed):
        print('zoom out.. ')
        self.zoom_speed = speed
        self.move_request_cont.Velocity.PanTilt.x = 0
        self.move_request_cont.Velocity.PanTilt.y = 0
        self.move_request_cont.Velocity.Zoom.x = -self.ZMAX * self.zoom_speed
        # self.move_request_cont.Timeout = timeout

        self.perform_move_cont(self.move_request_cont, timeout)

    def perform_move_cont(self, request, timeout):
        # Start continuous move
        self.ptz.ContinuousMove(request)
        # Wait a certain time
        sleep(timeout)
        # Stop continuous move
        self.ptz.Stop({'ProfileToken': request.ProfileToken})

    # ABSOLUTE MOTION
    def move_abs(self, angle_x, angle_y, angle_z):
        self.move_request_abs.Position.PanTilt.x = angle_x
        self.move_request_abs.Position.PanTilt.y = angle_y
        self.move_request_abs.Position.Zoom.x = angle_z             # zoom bug here

        # self.move_request_abs.Speed.PanTilt = [self.XMAX * self.pan_speed, self.YMAX * self.tilt_speed]
        # self.move_request_abs.Speed.Zoom = self.ZMAX * self.zoom_speed
        self.perform_move_abs(self.move_request_abs)

    def perform_move_abs(self, request):
        # Start absolute  move
        self.ptz.AbsoluteMove(request)
        # sleep(7)
        # Stop absolute  move
        # self.ptz.Stop({'ProfileToken': request.ProfileToken})

    # # # RELATIVE MOTION
    # def move_rel(self):
    #     print('move_abs .. ')
    #     self.move_request_rel.Translation.PanTilt.x = 0.1
    #     self.move_request_rel.Translation.PanTilt.y = 0.1
    #     #self.move_request_rel.Translation.Zoom.x = 0.1
    #
    #     # self.move_request_abs.Speed.PanTilt = [self.XMAX * self.pan_speed, self.YMAX * self.tilt_speed]
    #     # self.move_request_abs.Speed.Zoom = self.ZMAX * self.zoom_speed
    #     self.perform_move_rel(self.move_request_rel)
    #
    # def perform_move_rel(self, request):
    #     # Start absolute  move
    #     self.ptz.RelativeMove(request)
    #     # Stop absolute  move
    #     # self.ptz.Stop({'ProfileToken': request.ProfileToken})

    # GET POSITION
    def get_pose(self):
        start = time.time()
        pose = self.ptz.GetStatus(self.request_status).Position
        end = time.time()
        print('elapsed: ', end - start)
        pos_x = pose.PanTilt.x
        pos_y = pose.PanTilt.y
        pos_z = pose.Zoom.x
        print('x,y,z :', pos_x, pos_y, pos_z)
        return pos_x, pos_y, pos_z

    def get_move_status(self):
        start = time.time()
        pose = self.ptz.GetStatus(self.request_status)
        end = time.time()
        print('elapsed: ', end - start)
        return pose

    def get_time(self):
        ptz_utc_time = self.ptz.GetStatus(self.request_status).UtcTime
        ptz_time = {'year': ptz_utc_time.strftime("%Y"), 'month': ptz_utc_time.strftime("%m"),
                    'day': ptz_utc_time.strftime("%d"),
                    'hour': ptz_utc_time.strftime("%H"), 'minute': ptz_utc_time.strftime("%M"),
                    'second': ptz_utc_time.strftime("%S")}
        print('get time :', ptz_time)
        return ptz_time

    def move_home(self):
        print('Going to Home position ... ')
        self.ptz.GotoHomePosition(self.request_goto_home)
        # print('Home position: {}, {}, {}'.format(self.get_pose())

    # def get_dt(self):
    #     dt = self.device.devicemgmt.GetSystemDateAndTime()
    #     print('Dt: ', dt)
