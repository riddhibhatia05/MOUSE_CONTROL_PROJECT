import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode = False, maxHands = 2, complexity = 1, detectionCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # creating the hand detection obj
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode ,self.maxHands,
                                        self.complexity ,self.detectionCon,self .trackCon)

        # adding the mediapipe drawing utilities
        self.mpDraw = mp.solutions.drawing_utils


    def findHands(self, img, draw = True):
        #Drawing
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        # Hand Detection
        if self.results.multi_hand_landmarks:

            # Detecting the Hand Landmarks
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    # Drawing the Landmarks
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo = 0, draw = True):

        lmList = []

        # Measuring the size of the detection window
        if self.results.multi_hand_landmarks:

            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):

                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                lmList.append([id,cx,cy])
                # Drawing a Circle on one the fingers
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 255, 255), cv2.FILLED)

        return lmList

def main():

    # Fps initialization
    pTime = 0
    cTime = 0

    # Creating The video capture object
    cap = cv2.VideoCapture(0)

    detector = handDetector()

    # Main Loop
    while True:

        # image/cameraVideo Processing
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)

        # Fps Calculating System
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

        # Displaying the Window
        cv2.imshow("handtracker", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()