# from turtle import color
from cv2 import cvtColor,COLOR_BGR2HSV,inRange,createBackgroundSubtractorMOG2,erode,dilate,findContours,RETR_EXTERNAL,CHAIN_APPROX_SIMPLE,contourArea,moments,minEnclosingCircle,circle,imshow,VideoCapture,CAP_PROP_EXPOSURE,createBackgroundSubtractorKNN,waitKey,destroyAllWindows
import numpy as np
# import asyncio
import pandas as pd
import matplotlib.pyplot as plt
# import time
from threading import Event

from detect import crop
from ReadConfig import cam_port

x_data = []
y_data = []
##Another async function will go here to detect aruco and fix coordinate###

#Function for creating First mask(Using color)
async def generate_color_mask(frame):
    # Convert to HSV
    hsv = cvtColor(frame, COLOR_BGR2HSV)

    # Define red color range
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    # Create red mask
    mask1 = inRange(hsv, lower_red, upper_red)
    return mask1

#Function for creating second mask
fgbg = createBackgroundSubtractorMOG2()
# fgbg = cv2.createBackgroundSubtractorKNN()

def generate_background_mask(frame):
    global fgbg

    # Background subtraction
    fgmask = fgbg.apply(frame)
    return fgmask


#This Function Shows and returns data as arrays
def process_frame(frame, callback = None):
    global fgbg
    global x_data
    global y_data

    mask = generate_background_mask(frame)


#    mask = background_mask_task

    ###############Here I will apply the Aruko sticker method##############

    # Morphological operations (optional)
    kernel = np.ones((2,2), np.uint8)
    mask = erode(mask,None, iterations=1)
    mask = dilate(mask, None, iterations=2)

    # Find contours
    contours, _ = findContours(mask, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)

    # Find largest contour (assuming laser is the largest)
    if len(contours) in range(1,5):
        largest_contour = max(contours, key=contourArea)
        M = moments(largest_contour)
        if M["m00"] > 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            # Do something with the laser pointer position (cx, cy)
            (x_axis,y_axis),radius = minEnclosingCircle(largest_contour)
            center = (int(x_axis),int(y_axis))  
            radius = int(radius)
            print("Laser pointer position:", (cx/600, cy/300))
            if(callback is not None):
                callback(cx/600, cy/300)
            x_data.append(cx)
            y_data.append(cy)
            circle(frame,center,radius,(255,0,0),2)
    else:
        # print("Laser pointer position:", 0)
        x_data.append(0)
        y_data.append(0)
    if callback is None:
        imshow('frame', frame)
        imshow('mask', mask)
    return x_data, y_data
    

#This synchronous function makes pd dataframes and calculates results
def process_data(x_data,y_data):
    if len(x_data) == 0:
        return x_data
    
    x_data = np.array(x_data)
    y_data = np.array(y_data)

    df = pd.DataFrame({
        'X': x_data,
        'Y': y_data
    })

    # Identify indices where either X or Y is zero
    zero_indices = df[(df['X'] == 0) | (df['Y'] == 0)].index
    # Add a fake "end" index for easier processing
    zero_indices = zero_indices.to_list() + [len(df)]
    # Split the DataFrame and keep only the first row of each split
    split_dfs = []
    previous_index = 0
    for index in zero_indices:
        if previous_index != index:  # Ensure we are not adding empty splits
            split_dfs.append(df.iloc[previous_index])
        previous_index = index + 1

    # Combine the result into a new DataFrame
    result_df = pd.DataFrame(split_dfs)

    return df,result_df



def main(event, callback = None):
    global fgbg
    crp = False
    print("Test2")

    # cap = cv2.VideoCapture("/home/niccolo/ssim_practice/provided/2/two.mp4")
    # cap = cv2.VideoCapture("http://192.168.0.197:4747/video")
    cap = VideoCapture(cam_port)
    cap.set(CAP_PROP_EXPOSURE, 20)
    # fgbg = cv2.createBackgroundSubtractorMOG2()
    fgbg = createBackgroundSubtractorKNN()
    
    while True:
        if event.is_set():
            break
        ret, frame = cap.read()
        if not ret:
            break
        #frame_main = cv2.resize(frame,(600,300))
        frame = crop(frame)
        if frame is None:
            #frame = frame_main
            continue
        print("size => ", frame.shape[:2])
        # time.sleep(10)  ###Calibration time 5 seconds
        (x_data,y_data) = process_frame(frame, callback)
        df,result_df = process_data(x_data,y_data)

        if waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    destroyAllWindows()
    # print('X: ', x_data)
    # print('Y:', y_data)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)
    print(df)
    print(result_df)
    if callback is None:
        plt.scatter(result_df['X'],result_df['Y'], color='red')
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    event = Event()
    main(event)
