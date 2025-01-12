from cv2 import getPerspectiveTransform,warpPerspective,imread,cvtColor,COLOR_BGR2GRAY,line
import cv2.aruco as aruco
import numpy as np
top_left = None
top_right = None
bottom_left = None
bottom_right = None
warped = None

def Line(img, p1, p2):
        line(img, (int(p1[0]),int(p1[1])) ,(int(p2[0]),int(p2[1])), (255, 0, 0), 5)

def verify_point(point):
    if point is None:
        return False
    if len(point) != 2:
        return False
    return True
def cropImage(image):
    global top_left, top_right, bottom_left, bottom_right
    ok = verify_point(top_left) and verify_point(top_right) and verify_point(bottom_left) and verify_point(bottom_right)
    if not ok:
        return None
    # pts_src = np.array([[100, 100], [400, 100], [400, 300], [100, 300]])
    pts_src = np.array([top_left, top_right, bottom_right, bottom_left])

    # Define the width and height of the new image after perspective transformation
    # This is based on the desired output size
    width, height = 585, 275
    pts_dst = np.array([[0, 0], [width, 0], [width, height], [0, height]])

    # Compute the perspective transform matrix
    M = getPerspectiveTransform(pts_src.astype(np.float32), pts_dst.astype(np.float32))

    # Apply the perspective warp
    warped = warpPerspective(image, M, (width, height))
    return warped
def crop(image = None):
    global top_left, top_right, bottom_left, bottom_right
    # Load the image containing ArUco markers
    if(image is None):
        image = imread('result_1.png')
    warped = cropImage(image)
    if warped is not None:
        return warped
    # Convert the image to grayscale
    gray = cvtColor(image, COLOR_BGR2GRAY)

  
    # Define the dictionary for the type of markers used (e.g., DICT_4X4_50)
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

    # Initialize the detector parameters
    parameters = aruco.DetectorParameters()

    detector = aruco.ArucoDetector(aruco_dict,parameters)


    # Detect the markers in the image
    corners, ids, rejected_img_points = detector.detectMarkers(gray)
    
    
    # If markers are detected
    if ids is not None:
        # Draw the detected markers on the image
        # aruco.drawDetectedMarkers(image, corners, ids)
        
        # Print the detected marker IDs and their corner positions
        for i, marker_id in enumerate(ids):
            center = corners[i].mean(axis=1)[0]
            if marker_id[0] == 0:
                top_left = center
            elif marker_id[0] == 1:
                top_right = center
            elif marker_id[0] == 2:
                bottom_left = center
            elif marker_id[0] == 3:
                bottom_right = center
            
            print(f"Marker ID: {marker_id[0]}")
            print(f"Corners: {corners[i]}")
            print(f"Center: {corners[i].mean(axis=1)[0]}")  # Calculate center of marker
        if(len(ids) == 4):
            # line(image, top_left, top_right)
            # line(image, top_right, bottom_right)
            # line(image, bottom_right, bottom_left)
            # line(image, bottom_left, top_left)
            ok = verify_point(top_left) and verify_point(top_right) and verify_point(bottom_left) and verify_point(bottom_right)
            if not ok:
                return None
            # pts_src = np.array([[100, 100], [400, 100], [400, 300], [100, 300]])
            pts_src = np.array([top_left, top_right, bottom_right, bottom_left])

            # Define the width and height of the new image after perspective transformation
            # This is based on the desired output size
            width, height = 300, 300
            pts_dst = np.array([[0, 0], [width, 0], [width, height], [0, height]])

            # Compute the perspective transform matrix
            M = getPerspectiveTransform(pts_src.astype(np.float32), pts_dst.astype(np.float32))

            # Apply the perspective warp
            warped = warpPerspective(image, M, (width, height))


    else:
        print("No ArUco markers detected.")
    
    image = warped
    # Save or display the final image with markers detected
    # cv2.imwrite('detected_aruco_markers.png', image)
    # cv2.imshow('Detected ArUco Markers', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return image

if __name__ == '__main__':
    crop()
