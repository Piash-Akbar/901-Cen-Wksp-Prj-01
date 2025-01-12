from cv2 import cvtColor,threshold,THRESH_BINARY,COLOR_BGR2GRAY,bitwise_not,bitwise_and,addWeighted,imread,resize,imwrite,IMREAD_UNCHANGED
import numpy as np
import shutil

def overlay_image(background, overlay, x, y):
    # overlay = cv2.resize(overlay, (0, 0), fx=0.5, fy=0.5)
    overlay_height, overlay_width = overlay.shape[:2]

    # Ensure the overlay fits within the background dimensions
    if y + overlay_height > background.shape[0] or x + overlay_width > background.shape[1]:
        raise ValueError("Overlay image exceeds background dimensions.")

    # Create a region of interest (ROI) in the background image
    roi = background[y:y+overlay_height, x:x+overlay_width]

    # Convert images to float32 for accurate calculations
    background_float = roi.astype(np.float32)
    overlay_float = overlay.astype(np.float32)

    # Mask for detecting non-black pixels in the overlay
    mask = cvtColor(overlay, COLOR_BGR2GRAY)
    _, mask = threshold(mask, 1, 255, THRESH_BINARY)

    # Invert the mask to keep black areas
    mask_inv = bitwise_not(mask)

    # Handle alpha channel if present
    if overlay.shape[2] == 4:
        alpha_channel = overlay[:, :, 3] / 255.0  # Normalize alpha
        overlay_float = overlay_float[:, :, :3]  # Remove alpha channel

    # Preserve black areas from the overlay
    overlay_black = bitwise_and(overlay_float, overlay_float, mask=mask_inv)

    combined = bitwise_and(background_float, overlay_black)
    combined = addWeighted(combined, 1, overlay_float, 1, 0) + overlay_black
    

    # Convert back to uint8
    combined = np.clip(combined, 0, 255).astype(np.uint8)

    # Place the combined image back into the original background image
    background[y:y+overlay_height, x:x+overlay_width] = combined

    return background
def createImage(path):
    # Load images
    background = imread(path)
    # cv2.imwrite('main.png', background)
    
    # gray_image = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite('main_gray.png', gray_image)
    result_file = path.replace("bg", "result_bg")
    shutil.copyfile(result_file, "main.png")
    shutil.copyfile(result_file, "main_gray.png")
    
    # background = cv2.resize(background,(1024,512))
    top_left = imread('aruco_marker/aruco_marker_0.png', IMREAD_UNCHANGED)
    top_right = imread('aruco_marker/aruco_marker_1.png', IMREAD_UNCHANGED)
    bottom_left = imread('aruco_marker/aruco_marker_2.png', IMREAD_UNCHANGED)
    bottom_right = imread('aruco_marker/aruco_marker_3.png', IMREAD_UNCHANGED)
    height, width = background.shape[:2]

    marker_size = 68
    marker_half_size = 10

    top_left = resize(top_left, (marker_size, marker_size))
    top_right = resize(top_right, (marker_size, marker_size))
    bottom_left = resize(bottom_left, (marker_size, marker_size))
    bottom_right = resize(bottom_right, (marker_size, marker_size))

    # Overlay the image
    result = overlay_image(background, top_left, marker_half_size, marker_half_size)
    result = overlay_image(result, top_right, width-marker_size-marker_half_size, marker_half_size)
    result = overlay_image(result, bottom_left, marker_half_size, height-marker_size-marker_half_size)
    result = overlay_image(result, bottom_right, width-marker_size-marker_half_size, height-marker_size-marker_half_size)


    # Save or display the final image
    imwrite('result.png', result)

    # cv2.imshow('Overlay Image with Black Background', result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
