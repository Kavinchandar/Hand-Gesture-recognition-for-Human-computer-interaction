import math
import time
import numpy as np
import cv2
import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import matplotlib.pyplot as plt

test_time = []
test_fps = []


def fps(picture, prev_Time):
    current_Time = time.time()
    fps = 1 / (current_Time - prev_Time)
    prev_Time = current_Time
    test_time.append(current_Time//60)
    test_fps.append(fps)
    cv2.putText(picture, f'FPS: {int(fps)}', (10, 50),
                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
    return prev_Time


def volumebar(picture, volBar, volPer):
    cv2.rectangle(picture, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(picture, (50, int(volBar)), (85, 400),
                  (0, 255, 0), cv2.FILLED)
    cv2.putText(picture, f'{int(volPer)}%', (40, 450),
                cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)


def volumecontroller():
    width_Cam, height_Cam = 1000, 1000
    capture = cv2.VideoCapture(0)
    capture.set(3, width_Cam)
    capture.set(4, height_Cam)
    prev_Time = 0

    detector = htm.hand_Detector(detection_Con=0.7, track_Con=0.7)
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    volRange = volume.GetVolumeRange()
    min_vol = volRange[0]
    max_vol = volRange[1]
    vol = 0
    volBar = 0
    volPer = 0

    while True:
        success, picture = capture.read()
        picture = detector.find_Hands(picture, draw=True)
        Poslist = detector.find_Position(picture, draw=True)
        if Poslist:
            thumb_x, thumb_y = Poslist[4][1], Poslist[4][2]
            index_x, index_y = Poslist[8][1], Poslist[8][2]

            mid_x, mid_y = (thumb_x+index_x)//2, (thumb_y+index_y)//2
            cv2.line(picture, (thumb_x, thumb_y),
                     (index_x, index_y), (255, 0, 255), 2)
            cv2.circle(picture, (mid_x, mid_y), 6, (255, 0, 255), cv2.FILLED)

            # switch
            length = math.hypot(index_x-thumb_x, index_y-thumb_y)
            if length < 20:
                cv2.circle(picture, (mid_x, mid_y), 8, (0, 255, 0), cv2.FILLED)

            vol = np.interp(length, [20, 120], [min_vol, max_vol])
            volBar = np.interp(length, [20, 120], [400, 150])
            volPer = np.interp(length, [20, 120], [0, 100])
            volume.SetMasterVolumeLevel(vol, None)
            volumebar(picture, volBar, volPer)

        prev_Time = fps(picture, prev_Time)

        cv2.imshow('Gesture-based Volume Controller', picture)
        if cv2.waitKey(10) & 0xFF == ord('x'):
            break


if __name__ == '__main__':
    volumecontroller()
"""
plt.plot(test_time, test_fps)
plt.xlabel('Time (s)')
plt.ylabel('FPS')
plt.show()
"""
New_Colors = ['green', 'blue', 'purple', 'brown', 'teal']
plt.bar(test_fps, test_time, color=New_Colors)
plt.title('Gesture-based volume controller')
plt.xlabel('FPS')
plt.ylabel('Time (m)')
plt.show()
