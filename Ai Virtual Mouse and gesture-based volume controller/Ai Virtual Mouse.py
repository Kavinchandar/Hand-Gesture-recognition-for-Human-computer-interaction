import math
import cv2
import HandTrackingModule as htm
import pyautogui
import win32api
import time
import matplotlib.pyplot as plt
test_time = []
test_fps = []


def fps(picture, prev_Time):
    current_Time = time.time()
    fps = 1 / (current_Time - prev_Time)
    prev_Time = current_Time
    test_time.append(current_Time)
    test_fps.append(fps)
    cv2.putText(picture, f'FPS: {int(fps)}', (10, 50),
                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
    return prev_Time


def virtualMouse():
    width_Cam, height_Cam = 1000, 1000
    capture = cv2.VideoCapture(0)
    capture.set(10, width_Cam)
    capture.set(10, height_Cam)
    prev_Time = 0

    detector = htm.hand_Detector(detection_Con=0.7, track_Con=0.7)

    while True:
        success, picture = capture.read()
        picture = detector.find_Hands(picture, draw=True)
        poslist = detector.find_Position(picture, draw=True)

        if poslist:
            index_x, index_y = poslist[8][1], poslist[8][2]
            thumb_x, thumb_y = poslist[4][1], poslist[4][2]
            middle_x, middle_y = poslist[10][1], poslist[10][2]
            middle_knuckle_x, middle_knuckle_y = poslist[11][1], poslist[11][2]

            # cursor automation
            if index_x and index_y:
                win32api.SetCursorPos(
                    (index_x*5, index_y*5))

            # left click automation
            length_left_click = math.hypot(middle_x-thumb_x, middle_y-thumb_y)
            cv2.line(picture, (middle_x, middle_y),
                     (thumb_x, thumb_y), (255, 0, 0), 2)
            # print(length_left_click)
            if length_left_click < 20 and int(length_left_click) % 5 == 0:
                print("Left Click!")
                print()
                pyautogui.click()

            # right click automation
            length_right_click = math.hypot(
                middle_knuckle_x-thumb_x, middle_knuckle_y-thumb_y)
            cv2.line(picture, (middle_knuckle_x, middle_knuckle_y),
                     (thumb_x, thumb_y), (255, 0, 255), 2)
            # print(length_right_click)
            if length_right_click < 20 and int(length_right_click) % 5 == 0:
                print("Right Click!")
                print()
                pyautogui.click(button='right')

        # fps automation
        prev_Time = fps(picture, prev_Time)

        cv2.imshow('AI virtual Mouse', picture)
        if cv2.waitKey(10) & 0xFF == ord('x'):
            break


if __name__ == "__main__":
    virtualMouse()

New_Colors = ['green', 'blue', 'purple', 'brown', 'teal']
plt.bar(test_fps, test_time, color=New_Colors)
plt.title('AI Virtual Mouse')
plt.xlabel('FPS')
plt.ylabel('Time (m)')
plt.show()
