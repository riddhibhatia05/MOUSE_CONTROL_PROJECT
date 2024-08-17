Project Overview

Objective:
To create a system that allows users to control their computer's mouse using hand movements and gestures detected through a webcam.

Technologies Used:
OpenCV: This is used to capture video from the webcam and process the video frames.
NumPy: For numerical operations and coordinate transformations.
HandTrackingModule: A custom module (likely based on MediaPipe) for detecting and tracking hand landmarks.
pyautogui: This is used to control mouse movements and clicks.
Time: This is used to calculate and display the frames per second (FPS).

Detailed Explanation
1. Initialization
Camera Setup:
The webcam is initialized to capture video with specified width (wCam) and height (hCam).
The camera frame size is set to 640x480 pixels.
Hand Detector:
A hand detector is initialized to detect a maximum of one hand at a time.
The screen size is obtained using pyautogui.size() to map the hand movements to screen coordinates.
Constants and Variables:
frameR is the frame reduction to create a boundary within which hand movements are tracked.
smoothening is a factor to smooth out cursor movements.
pTime, plocX, plocY, clocX, and clocY are variables used for calculating FPS and smoothing cursor movement.
2. Main Loop
The main loop continuously captures frames from the webcam and processes them to track hand movements and perform actions based on gestures.
Capture Frame:
A frame is captured from the webcam.
Hand landmarks are detected in the frame using the hand detector.
Find Hand Landmarks:
If hand landmarks are detected, the positions of the index and middle fingers are obtained.
Check Fingers Up:
The fingersUp method determines which fingers are up.
A rectangle is drawn on the frame to show the boundary within which the hand should move.
3. Moving Mode (Index Finger Up)
When only the index finger is up:
Convert Coordinates:
The index finger tip coordinates are converted from camera frame coordinates to screen coordinates using np.interp.
Smoothen Values:
The cursor movement is smoothed using a weighted average.
Move Mouse:
The mouse cursor is moved to the new coordinates using pyautogui.moveTo.
A circle is drawn on the frame at the index finger tip to visualize the tracking.
4. Clicking Mode (Index and Middle Fingers Up)
When both the index and middle fingers are up:
Find Distance:
The distance between the tips of the index and middle fingers is calculated.
Click Mouse:
If the distance is below a certain threshold, a mouse click is performed using pyautogui.click.
A circle is drawn on the frame to indicate the click action.
5. Display FPS
Calculate FPS:
The frames per second (FPS) is calculated to monitor the performance.
Display FPS:
The FPS is displayed on the frame using cv2.putText.
6. Display the Image
Show Frame:
The processed frame is displayed in a window using cv2.imshow.
Functions
main: The main function that initializes variables and runs the main loop.
move_mouse: Handles the cursor movement based on index finger position.
click_mouse: Handles the mouse click action when both index and middle fingers are up.
display_fps: Calculates and displays the FPS on the frame.

Execution
The script runs by calling the main function, which handles the entire process of capturing frames, detecting hand gestures, and controlling the mouse.

Conclusion
This project demonstrates how computer vision and hand tracking can be used to create a touchless interface for controlling a computer. It leverages various libraries to process video input, detect hand landmarks, and perform mouse actions based on specific gestures. This kind of technology has potential applications in areas where touchless control is advantageous, such as in hygienic environments or for accessibility purposes.







