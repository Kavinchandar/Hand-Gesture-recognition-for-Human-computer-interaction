import time
import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
# test
test_time = []
test_fps = []


class hand_Detector():
    def __init__(self, mode=False, max_Hands=1, detection_Con=0.7, track_Con=0.7):
        self.mode = mode
        self.max_Hands = max_Hands
        self.detection_Con = detection_Con
        self.track_Con = track_Con
        self.mp_Hands = mp.solutions.hands
        self.hands = self.mp_Hands.Hands(
            self.mode, self.max_Hands, self.detection_Con, self.track_Con)
        self.mp_Draw = mp.solutions.drawing_utils

    def find_Hands(self, image, draw=True):
        imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLandmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_Draw.draw_landmarks(
                        image, handLandmarks, self.mp_Hands.HAND_CONNECTIONS,
                        self.mp_Draw.DrawingSpec(
                            color=(0, 0, 0), thickness=1, circle_radius=2))
        return image

    def find_Position(self, image, handNo=0, draw=True):
        posList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, pt in enumerate(myHand.landmark):
                h, w, c = image.shape
                c = None
                id_x, id_y = int(pt.x*w), int(pt.y*h)
                posList.append([id, id_x, id_y])
                if draw:
                    cv2.circle(image, (id_x, id_y), 1, (0, 0, 0), cv2.FILLED)
        return posList


def fps(picture, prev_Time):
    current_Time = time.time()
    fps = 1 / (current_Time - prev_Time)
    prev_Time = current_Time
    test_time.append(current_Time)
    test_fps.append(fps)
    cv2.putText(picture, f'FPS: {int(fps)}', (10, 50),
                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
    return prev_Time


def display():
    prev_Time = 0
    capture = cv2.VideoCapture(0)
    detector = hand_Detector()
    while True:
        success, image = capture.read()
        image = detector.find_Hands(image)
        posList = detector.find_Position(image)
        if posList:
            print(posList)
        prev_Time = fps(image, prev_Time)
        cv2.imshow("Hand Tracker", image)
        if cv2.waitKey(10) & 0xFF == ord('x'):
            break


if __name__ == "__main__":
    display()
    start_time = time.time()
    print("--- %s seconds ---" % (time.time() - start_time))
#print(sum(test)//len(test), "Frames per second on average")

New_Colors = ['green', 'blue', 'purple', 'brown', 'teal']
plt.bar(test_fps, test_time, color=New_Colors)
plt.title('Hand Tracking Module')
plt.xlabel('FPS')
plt.ylabel('Time (m)')
plt.show()
