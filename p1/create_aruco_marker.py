from cv2 import cvtColor,COLOR_GRAY2BGR,imwrite,aruco
# import cv2.aruco as aruco
import numpy as np

# Define parameters
marker_size = 200  # Size of the marker in pixels
marker_id = 0      # Marker ID from 0 to 50 for DICT_4X4_50
total_markers = 10  # Number of markers to generate
background_color = (255, 255, 255)  # Background color in BGR (white)

# Create the dictionary
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

# Generate and save each marker
for marker_id in range(total_markers):
    marker_image = np.zeros((marker_size, marker_size, 3), dtype=np.uint8)
    
    # Set the background color
    marker_image[:] = background_color

    # Generate the ArUco marker
    aruco_marker = aruco.generateImageMarker(aruco_dict, marker_id, marker_size)

    # Convert the marker to 3 channels
    aruco_marker = cvtColor(aruco_marker, COLOR_GRAY2BGR)

    # Overlay the marker onto the colored background
    marker_with_background = np.where(aruco_marker == 0, aruco_marker, marker_image)

    # Save the marker with the background color
    filename = f"aruco_marker/aruco_marker_{marker_id}.png"
    imwrite(filename, marker_with_background)
    print(f"Marker {marker_id} with background saved as {filename}")
