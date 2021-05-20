import math
import yaml
from PyQt5 import QtCore, QtGui, QtWidgets
from onvif import ONVIFCamera
from utils import PTZ


class CameraView(QtWidgets.QGraphicsView):
    image_clicked = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent):
        super(CameraView, self).__init__(parent)
        # self.zoom = 0

        self.frame = QtWidgets.QGraphicsScene(self)
        self.image = QtWidgets.QGraphicsPixmapItem()
        self.frame.addItem(self.image)
        self.setScene(self.frame)

        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(10, 10, 10)))
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

        # self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.setFrameShape(QtWidgets.QFrame.NoFrame)

    # def fitInView(self, scale=True):
    #     rect = QtCore.QRectF(self.image.pixmap().rect())
    #     if not rect.isNull():
    #         self.setSceneRect(rect)
    #         unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
    #         self.scale(1 / unity.width(), 1 / unity.height())
    #         viewrect = self.viewport().rect()
    #         scenerect = self.transform().mapRect(rect)
    #         factor = min(viewrect.width() / scenerect.width(),
    #                      viewrect.height() / scenerect.height())
    #         self.scale(factor, factor)
    #         self.zoom = 0

    # def wheelEvent(self, event):
    #     if event.angleDelta().y() > 0:
    #         factor = 1.25
    #         self.zoom += 1
    #     else:
    #         factor = 0.8
    #         self.zoom -= 1
    #
    #     if self.zoom > 0:
    #         self.scale(factor, factor)
    #     elif self.zoom == 0:
    #         self.fitInView()
    #     else:
    #         self.zoom = 0

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            coef = 1.25
        else:
            coef = 0.8
        self.scale(coef, coef)

    def mouseDoubleClickEvent(self, event):
        if self.image.isUnderMouse():
            self.image_clicked.emit(self.mapToScene(event.pos()).toPoint())
        super(CameraView, self).mousePressEvent(event)


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()

        # self.zoomx = 0

        self.viewer = CameraView(self)

        self.viewer.image.setPixmap(QtGui.QPixmap('data/Astana_small.png'))
        self.viewer.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

        # self.viewer.zoom = 0
        # self.viewer.fitInView()

        self.viewer.image_clicked.connect(self.change_pose)

        # 'button_zoom_in' button
        self.button_zoom_in = QtWidgets.QToolButton(self)
        self.button_zoom_in.setText('zoom in')
        self.button_zoom_in.clicked.connect(self.zoom_in)

        # 'button_zoom_out' button
        self.button_zoom_out = QtWidgets.QToolButton(self)
        self.button_zoom_out.setText('zoom out')
        self.button_zoom_out.clicked.connect(self.zoom_out)

        # 'button_move_up' button
        self.button_move_up = QtWidgets.QToolButton(self)
        self.button_move_up.setText('move up')
        self.button_move_up.clicked.connect(self.move_up)

        # 'button_move_down' button
        self.button_move_down = QtWidgets.QToolButton(self)
        self.button_move_down.setText('move down')
        self.button_move_down.clicked.connect(self.move_down)

        # 'button_move_right' button
        self.button_move_right = QtWidgets.QToolButton(self)
        self.button_move_right.setText('move right')
        self.button_move_right.clicked.connect(self.move_right)

        # 'button_move_left' button
        self.button_move_left = QtWidgets.QToolButton(self)
        self.button_move_left.setText('move left')
        self.button_move_left.clicked.connect(self.move_left)

        # 'button_check_pose' button
        self.button_check_pose = QtWidgets.QToolButton(self)
        self.button_check_pose.setText('Get position')
        self.button_check_pose.clicked.connect(self.check_pose)

        # box pose
        self.line_pose = QtWidgets.QLineEdit(self)
        self.line_pose.setReadOnly(True)
        self.line_pose.setFixedWidth(200)

        # box pan
        self.line_pan = QtWidgets.QLineEdit(self)
        self.line_pan.setReadOnly(True)
        self.line_pan.setFixedWidth(35)
        self.line_pan.setText(str(config['pan_speed'] * 100))

        # box tilt
        self.line_tilt = QtWidgets.QLineEdit(self)
        self.line_tilt.setReadOnly(True)
        self.line_tilt.setFixedWidth(35)
        self.line_tilt.setText(str(config['tilt_speed'] * 100))

        # box zoom
        self.line_zoom = QtWidgets.QLineEdit(self)
        self.line_zoom.setReadOnly(True)
        self.line_zoom.setFixedWidth(35)
        self.line_zoom.setText(str(config['zoom_speed'] * 100))

        # labels
        self.label_pan = QtWidgets.QLabel("Pan speed: ")
        self.label_tilt = QtWidgets.QLabel("Tilt speed: ")
        self.label_zoom = QtWidgets.QLabel("Zoom speed: ")
        self.label_empty = QtWidgets.QLabel(" ")
        self.label_pan.setFixedWidth(60)
        self.label_tilt.setFixedWidth(60)
        self.label_zoom.setFixedWidth(60)
        self.label_empty.setFixedWidth(100)

        # pan velocity slider
        self.slider_velx = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_velx.setMinimum(0)
        self.slider_velx.setMaximum(100)
        self.slider_velx.setValue(config['pan_speed']*100)
        self.slider_velx.setTickInterval(100)
        self.slider_velx.setFixedWidth(100)
        self.slider_velx.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider_velx.valueChanged.connect(self.vel_pan)

        # tilt velocity slider
        self.slider_vely = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_vely.setMinimum(0)
        self.slider_vely.setMaximum(100)
        self.slider_vely.setValue(config['tilt_speed'] * 100)
        self.slider_vely.setTickInterval(100)
        self.slider_vely.setFixedWidth(100)
        self.slider_vely.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider_vely.valueChanged.connect(self.vel_tilt)

        # zoom velocity slider
        self.slider_velz = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_velz.setMinimum(0)
        self.slider_velz.setMaximum(100)
        self.slider_velz.setValue(config['zoom_speed'] * 100)
        self.slider_velz.setTickInterval(100)
        self.slider_velz.setFixedWidth(100)
        self.slider_velz.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider_velz.valueChanged.connect(self.vel_zoom)

        # Arrange layout

        layout_widget = QtWidgets.QHBoxLayout()
        layout_widget.setAlignment(QtCore.Qt.AlignLeft)

        layout_widget.addWidget(self.button_check_pose)
        layout_widget.addWidget(self.line_pose)
        layout_widget.addWidget(self.label_empty)

        layout_widget.addWidget(self.label_pan)
        layout_widget.addWidget(self.slider_velx)
        layout_widget.addWidget(self.line_pan)
        layout_widget.addWidget(self.button_move_left)
        layout_widget.addWidget(self.button_move_right)
        layout_widget.addWidget(self.label_empty)

        layout_widget.addWidget(self.label_tilt)
        layout_widget.addWidget(self.slider_vely)
        layout_widget.addWidget(self.line_tilt)
        layout_widget.addWidget(self.button_move_up)
        layout_widget.addWidget(self.button_move_down)
        layout_widget.addWidget(self.label_empty)

        layout_widget.addWidget(self.label_zoom)
        layout_widget.addWidget(self.slider_velz)
        layout_widget.addWidget(self.line_zoom)
        layout_widget.addWidget(self.button_zoom_in)
        layout_widget.addWidget(self.button_zoom_out)

        layout_image = QtWidgets.QVBoxLayout(self)
        layout_image.addWidget(self.viewer)
        layout_image.addLayout(layout_widget)

    def zoom_in(self):
        ptz_object.zoom_in_cont(timeout=1/2, speed=self.slider_velz.value()/100)

    def zoom_out(self):
        ptz_object.zoom_out_cont(timeout=1/2, speed=self.slider_velz.value()/100)

    def move_up(self):
        ptz_object.move_up_cont(timeout=1, speed=self.slider_vely.value()/100)

    def move_down(self):
        ptz_object.move_down_cont(timeout=1, speed=self.slider_vely.value()/100)

    def move_right(self):
        ptz_object.move_right_cont(timeout=1, speed=self.slider_velx.value()/100)

    def move_left(self):
        ptz_object.move_left_cont(timeout=1, speed=self.slider_velx.value()/100)

    def check_pose(self):
        pose_x, pose_y, pose_z = ptz_object.get_pose()
        self.line_pose.setText('pan: {:.3f}, tilt: {:.3f}, zoom: {:.3f}'.format(pose_x, pose_y, pose_z))

    def vel_pan(self):
        self.line_pan.setText(str(self.slider_velx.value()))

        # config['pan_speed'] = self.slider_velx.value()/100

    def vel_tilt(self):
        self.line_tilt.setText(str(self.slider_vely.value()))

        # config['tilt_speed'] = self.slider_vely.value()/100

    def vel_zoom(self):
        self.line_zoom.setText(str(self.slider_velz.value()))
        # config['zoom_speed'] = self.slider_velz.value()/100

    def change_pose(self, pos):
        print('Go to next position --> ', pos.x(), pos.y())

        x0 = 2695
        y0 = 4019

        x1 = pos.x()
        y1 = pos.y()

        angle = math.atan2(y1-y0, x1-x0)
        # angle [-pi , pi]

        angle_calib = angle - 1.02

        # angle should be between -pi and pi
        if angle_calib < -3.14:
            angle_calib = 6.28 + angle_calib

        angle_calib = angle_calib/3.14

        # calculate tilt angle
        rad = math.sqrt((y1-y0)**2 + (x1-x0)**2)

        angle_calib_y = math.atan(rad/32)

        angle_calib_y = -(1.57 - angle_calib_y)

        if angle_calib_y <= -0.785:
            angle_calib_y = -1
        elif angle_calib_y >= 0.348:
            angle_calib_y = 1
        # option 1
        elif -0.785 < angle_calib_y <= 0:
            angle_calib_y = angle_calib_y/0.785
        else:
            # 0 < angle_calib_y < 0.785:
            angle_calib_y = angle_calib_y / 0.348

        # option 2
        # else:
        #     angle_calib_y = (angle_calib_y - (-0.348))*2/1.133 - 1
        # print('angle_calib_y: ', angle_calib_y)

        ptz_object.move_abs(angle_calib, angle_calib_y, 0.2)


if __name__ == '__main__':

    import sys

    # get the config params
    config = yaml.safe_load(open("config.yml"))
    config_user = yaml.safe_load(open("config_user.yml"))

    # Define the onvif device
    onvif_device = ONVIFCamera(config_user['ip'], 80, config_user['login'], config_user['password'], 'python-onvif-zeep/wsdl/')

    # create the ptz class
    ptz_object = PTZ(onvif_device)

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setGeometry(200, 200, 900, 700)
    window.show()
    sys.exit(app.exec_())
