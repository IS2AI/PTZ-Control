"""
This script allows to save the video using the configuration in config file.
"""

import cv2
import yaml


def save_video():
    config = yaml.safe_load(open("config.yml"))
    config_user = yaml.safe_load(open("config_user.yml"))
    cap = cv2.VideoCapture('rtsp://'+config_user['ip']+':554/stream1')

    # Default resolutions of the frame are obtained.The default resolutions are system dependent.
    # We convert the resolutions from float to integer.
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # get the params to save video
    video_save = config['video_save']
    video_path = config['video_path']
    video_name = config['video_name']
    video_fps = config['video_fps']

    if video_save:
        print('Writing the video to file... : ', video_path + video_name + '.avi')

    # Define the codec and create VideoWriter object.
    out = cv2.VideoWriter(video_path + video_name + '.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), video_fps,
                          (frame_width, frame_height))

    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error opening video stream or file")

    # Read until video is completed
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:

            # Display the resulting frame
            cv2.imshow('Frame', frame)

            if video_save:
                # write to file
                out.write(frame)

            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break

    # When everything done, release the video capture object
    cap.release()
    out.release()

    # Closes all the frames
    cv2.destroyAllWindows()


if __name__ == '__main__':
    save_video()
