# put image files in folder "image"
# python 01_binary_test.py --input [file]
# python 01_binary_test.py --input test.jpg

import cv2 as cv
import numpy as np
import os
import argparse


def calculate_distance(point1, point2):
    return np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def mouse_callback(event, x, y, flags, param):
    global points, distances

    if event == cv.EVENT_LBUTTONDOWN:
        if len(points) % 2 == 0:
            points.append((x,y))
            cv.circle(temp_img, center=(x,y), radius=4, color=(255, 0, 0), thickness=-1)
        else:
            points.append((x,y))
            cv.circle(temp_img, (x,y), 3, (0, 255, 0), -1 )
            if len(points) > 1 and len(points) % 2 == 0:
                start_point = points[-2]
                end_point = points[-1]
                cv.line(temp_img, pt1=start_point, pt2=end_point, color=(255, 255, 255), thickness=2)
                distance = calculate_distance(start_point, end_point)
                distances.append(distance)
                print(f'두 점 사이의 거리는 : {len(points)//2}번 {distance}')
                cv.putText(temp_img, f'Distance {len(points)//2}: {distance:.3f}', (start_point[0], start_point[1]-10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

points = []
distances = []

parser = argparse.ArgumentParser(description='Draw lines and calculate distances')
parser.add_argument('--input', required=True, help='Input image file path')
args = parser.parse_args() # args Namespace(input='test.jpg')

input_file = args.input # test.jpg
input_filename, extension = input_file.split('.') # test, jpg
input_path = 'image'
output_path = 'result'
output_file = os.path.join(output_path, f'{input_filename}.png') # result/test.png

img = cv.imread(os.path.join(input_path, input_file), cv.IMREAD_COLOR)
temp_img = img.copy()
cv.namedWindow('Length of lines')
cv.setMouseCallback('Length of lines', mouse_callback)

while True:
    
    text = 'Image initialize if press "Space bar" key'
    cv.putText(temp_img, text=text, org=(15, 20), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 255))
    cv.imshow('Length of lines', temp_img)
    
    key = cv.waitKey(1)
    if key == 27: # esc key
        break
    elif key ==13:
        cv.imwrite(os.path.join(output_path, f'{input_filename}_lines.png'),temp_img)
    elif key == 32: # spacebar key
        temp_img = img.copy() # initialize screen

cv.destroyAllWindows()