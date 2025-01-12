import cv2
from cv2 import line, circle, VideoCapture, imshow, waitKey, destroyAllWindows, aruco, WND_PROP_VISIBLE, getWindowProperty
import numpy as np
from ReadConfig import cam_port

top_left = None
top_right = None
bottom_left = None
bottom_right = None
warped = None

def verify_point(point):
    if point is None:
        return False
    if len(point) != 2:
        return False
    return True

def aruco_detect(image):   
    global top_left, top_right, bottom_left, bottom_right
    # Define the dictionary for the type of markers used (e.g., DICT_4X4_50)
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    # Initialize the detector parameters
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict, parameters)
    # Detect the markers in the image
    corners, ids, rejected_img_points = detector.detectMarkers(image)

    # If markers are detected
    if ids is not None:
        aruco.drawDetectedMarkers(image, corners, ids)
        # Calculate and draw center points for each detected marker
        for corner in corners:
            # Convert the corner points to a numpy array
            corner_points = np.array(corner[0], dtype=np.float32)
            # Compute the center of the marker
            center_x = np.mean(corner_points[:, 0])
            center_y = np.mean(corner_points[:, 1])
            center = (int(center_x), int(center_y))
            # Draw a circle at the center of the marker
            circle(image, center, 5, (0, 2, 255), -1)
    else:
        print("No ArUco markers detected.")

    return image

cap = VideoCapture(cam_port)

while True:
    _, frame = cap.read()
    # Detect ArUco markers in the frame
    frame = aruco_detect(frame)
    
    # Display the frame
    imshow('Detected ArUco Markers', frame)

    # Check if the window is closed or the 'q' key is pressed to exit
    key = waitKey(1)
    if key == ord('q'):  # Press 'q' to quit
        break

    # Optional: Check window visibility (but you can rely on 'q' for exiting)
    if getWindowProperty('Detected ArUco Markers', WND_PROP_VISIBLE) < 1:
        break

# Release the capture object and destroy all windows
cap.release()  # Fix: Add parentheses to call release()
destroyAllWindows()


