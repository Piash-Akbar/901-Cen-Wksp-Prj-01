from cv2 import imread,circle,imwrite 


marker_size = 68
padding = 10
def saveImage(xr, yr):
    image = imread('main.png')
    height, width = image.shape[:2]
    print("save size =>", width, height)
    ref_w = width - 2*padding - marker_size//2
    ref_h = height - 2*padding - marker_size//2
    x = padding + marker_size//2 + int(ref_w*xr)
    y = padding + marker_size//2 + int(ref_h*yr)

    center = (x , y)
    image = circle(image,center, 2,(0,0,255),5)
    imwrite("result_data.png",image)

def saveImageAllpoints(points = []):
    final_points = []
    print("Points -> ")
    image = imread('main_gray.png')
    height, width = image.shape[:2]
    for p in points:
        print(p)
        xr, yr = p
        ref_w = width - 2*padding - marker_size//2
        ref_h = height - 2*padding - marker_size//2
        x = padding + marker_size//2 + int(ref_w*xr)
        y = padding + marker_size//2 + int(ref_h*yr)
        center = (x , y)
        final_points.append(center)
        image = circle(image,center,2,(0,0,255),5)
    imwrite("result_data.png",image)
    return final_points


