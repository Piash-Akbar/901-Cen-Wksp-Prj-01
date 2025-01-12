from cv2 import imread,cvtColor,COLOR_BGR2GRAY,GaussianBlur,Canny,findContours,RETR_EXTERNAL,CHAIN_APPROX_SIMPLE,contourArea,drawContours,FILLED,dilate,circle,FONT_HERSHEY_SIMPLEX,putText,LINE_AA,waitKey,destroyAllWindows,imshow
import numpy as np


def DataProcess(res_img, res_array):
  img = imread(res_img)
  gray = cvtColor(img, COLOR_BGR2GRAY)
  blur = GaussianBlur(gray, (5, 5), 0)
  edged = Canny(blur, 10, 250)
  contours, hierarchy = findContours(edged, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)

  # Find the two largest contours
  contours = sorted(contours, key=contourArea, reverse=True)[:2]

  # Create a mask
  mask = np.zeros_like(gray)
  drawContours(mask, contours, -1, (255), thickness=FILLED)

  # Apply dilation to close small holes in the mask
  kernel = np.ones((3, 3), np.uint8)
  mask = dilate(mask, kernel, iterations=1)  # Adjust iterations as needed

      # Find the contours of the white-bordered area
  contours_white_border,_ = findContours(mask, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)

  drawContours(mask, contours_white_border, -1, (255), thickness=FILLED)


  # imshow("mask", mask)

  # Initialize a list to store coordinates with non-black pixels
  filtered_res = []

  # Check each coordinate
  for (x, y) in res_array:
      # Ensure coordinates are within image bounds
      if x >= 0 and y >= 0 and x < mask.shape[1] and y < mask.shape[0]:
          # Get the pixel value at the coordinate
          pixel_value = mask[y, x]

          # Check if the pixel value is black
          if not (pixel_value == 0):
              # If not black, add to filtered coordinates
              filtered_res.append((x, y))
      else:
          print(f"Warning: Coordinate ({x}, {y}) is out of image bounds.")

  # Calculate the midpoint of the image
  midpoint_x = img.shape[1] // 2

  # Initialize lists for left and right sides
  left_side = []
  right_side = []

  # Separate coordinates based on left or right side
  for x, y in filtered_res:
    if x < midpoint_x:
      left_side.append((x, y))
    else:
      right_side.append((x, y))

  # Plot the points on the image
  # img = imread(res_img)
  for x, y in left_side:
    circle(img, (x, y), 5, (0, 0, 255), -1)  # Red for left side
  for x, y in right_side:
    circle(img, (x, y), 5, (0, 255, 0), -1)  # Green for right side

  # Display the number of points on each side
  font = FONT_HERSHEY_SIMPLEX
  putText(img, f"Left: {len(left_side)}", (180, img.shape[0] - 70), font, 1, (0, 0, 255), 2, LINE_AA)
  putText(img, f"Right: {len(right_side)}", (img.shape[1] - 310, img.shape[0] - 70), font, 1, (0, 255, 0), 2, LINE_AA)

  # Display the image
  # imshow("Result", res_img)

  # Wait for any key to be pressed
  waitKey(0)

  # Close all OpenCV windows
  destroyAllWindows()

  return img, left_side, right_side



if __name__ == "__main__":
  ###########Run the function##############
  res_array = [(280,300),(767,121),(800,280),(210,259),(293,230),(765,267),(358,161)]
  res_img = './main.png'
  res_img,left_side, right_side = DataProcess(res_img,res_array)

  print(left_side,right_side)
  imshow("Result",res_img)
  # Wait for any key to be pressed
  waitKey(0)

  # Close all OpenCV windows
  destroyAllWindows()








