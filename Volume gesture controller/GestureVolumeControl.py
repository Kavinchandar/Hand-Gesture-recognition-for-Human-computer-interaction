import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
min_vol = volRange[0]
max_vol = volRange[1]
vol = 0
volBar = 0
volPer = 0
# HAND RANGE 20 to 120
# VOLUME RANGE -64 to 0

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=True)
    lmlist = detector.findPosition(img, draw=False)
    if len(lmlist) != 0:
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2
        cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 8, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
        cv2.circle(img, (cx, cy), 6, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        if length < 20:
            cv2.circle(img, (cx, cy), 8, (0, 255, 0), cv2.FILLED)

        vol = np.interp(length, [20, 120], [min_vol, max_vol])
        volBar = np.interp(length, [20, 120], [400, 150])
        volPer = np.interp(length, [20, 120], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)

        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400),
                      (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(volPer)}%', (40, 450),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (10, 50),
                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)

    cv2.imshow('Gesture Volume Controller', img)
    cv2.waitKey(1)
