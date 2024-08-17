import cv2
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui

# Constants
wCam, hCam = 640, 480
frameR = 100  # Frame Reduction
smoothening = 7

# Variables
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# Initialize Camera
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Initialize Hand Detector
detector = htm.handDetector(maxHands=1)
wScr, hScr = pyautogui.size()

def main():
    global pTime, plocX, plocY, clocX, clocY

    while True:
        # 1. Find hand Landmarks
        success, img = cap.read()
        if not success:
            continue
        
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)

        # 2. Get the tip of the index and middle fingers
        if lmList:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]

            # 3. Check which fingers are up
            fingers = detector.fingersUp()

            # Draw the boundary box for hand movement
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 255, 255), 2)

            # 4. Only Index Finger : Moving Mode
            if fingers[1] == 1 and fingers[2] == 0:
                move_mouse(x1, y1, img)

            # 5. Both Index and middle fingers are up : Clicking Mode
            if fingers[1] == 1 and fingers[2] == 1:
                click_mouse(x1, y1, x2, y2, img)

        # 6. Display Frame Rate
        display_fps(img)

        # 7. Display the Image
        cv2.imshow("Image", img)
        cv2.waitKey(1)

def move_mouse(x1, y1, img):
    global plocX, plocY, clocX, clocY

    # Convert Coordinates
    x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
    y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

    # Smoothen Values
    clocX = plocX + (x3 - plocX) / smoothening
    clocY = plocY + (y3 - plocY) / smoothening

    # Move Mouse
    pyautogui.moveTo(wScr - clocX, clocY)
    cv2.circle(img, (x1, y1), 15, (255, 243, 0), cv2.FILLED)
    plocX, plocY = clocX, clocY

def click_mouse(x1, y1, x2, y2, img):
    # Find distance between fingers
    length, img, lineInfo = detector.findDistance(8, 12, img)

    # Click mouse if distance short
    if length < 40:
        cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
        pyautogui.click()

def display_fps(img):
    global pTime

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

if __name__ == "__main__":
    main()
