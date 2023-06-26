# put image files in folder "image"
# python 01_binary_test.py --input [file]
# python 01_binary_test.py --input test.jpg

import cv2 as cv
import numpy as np
import os
import argparse

def calculate_angle(line1, line2):
    vector1 = np.array([line1[2] - line1[0], line1[3] - line1[1]])
    vector2 = np.array([line2[2] - line2[0], line2[3] - line2[1]])
    dot_product = np.dot(vector1, vector2)
    print(dot_product)
    magnitude1 = np.linalg.norm(vector1) # length of vector
    magnitude2 = np.linalg.norm(vector2)
    cos_theta = dot_product / (magnitude1 * magnitude2)
    radian = np.arccos(cos_theta)
    theta = np.degrees(radian) # translate from radian to degree
    theta = np.fmin(theta, 180.0 - theta) # present acute angle

    return theta

def mouse_callback(event, x, y, flags, param):
    global count, x0, y0, lines, thetas

    if event == cv.EVENT_FLAG_LBUTTON:
        count = count + 1

        if count % 2 == 0:
            cv.circle(temp_img, (x, y), 4, (255, 0, 0), -1)
            cv.line(temp_img, (x0, y0), (x, y), (255, 255, 255), 2)  

            lines.append([x0, y0, x, y])
            cv.circle(temp_img, (x, y), 4, (0, 255, 0), -1)
            if len(lines) == 2:
                line1 = lines[-2]
                line2 = lines[-1]
                cv.line(temp_img, (line1[0], line1[1]), (line1[2], line1[3]), (255, 255, 255), 2)
                cv.line(temp_img, (line2[0], line2[1]), (line2[2], line2[3]), (255, 255, 255), 2)
                theta = calculate_angle(line1, line2)
                thetas.append(theta)  # theta 값을 thetas 리스트에 추가합니다.
                text_position = ((line1[0] + line1[2]) // 2, (line1[1] + line1[3]) // 2)
                cv.putText(temp_img, f'Angle {len(thetas)}: {theta:.3f}', text_position, cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                count = 0
                lines.clear()

        else:
            x0 = x
            y0 = y
            cv.circle(temp_img, (x, y), 4, (255, 0, 0), -1)

count = 0
x0 = -1
y0 = -1
lines = []
thetas = []

parser = argparse.ArgumentParser(description='Draw lines and calculate angles')
parser.add_argument('--input', required=True, help='Input image file path')
args = parser.parse_args() # args Namespace(input='test.jpg')

input_file = args.input # test.jpg
input_filename, extension = input_file.split('.') # test, jpg
input_path = 'image'
output_path = 'result'
output_file = os.path.join(output_path, f'{input_filename}.png') # result/test.png

img = cv.imread(os.path.join(input_path, input_file), cv.IMREAD_COLOR)
temp_img = img.copy()
cv.namedWindow('Angle of 2 lines')
cv.setMouseCallback('Angle of 2 lines', mouse_callback)

while True:
    text = 'Image initialize if press "Space bar" key'
    cv.putText(temp_img, text=text, org=(15, 20), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 255))
    cv.imshow('Angle of 2 lines', temp_img)
    
    key = cv.waitKey(1)
    if key == 27: # esc key
        break
    elif key == 13:
        cv.imwrite(os.path.join(output_path, f'{input_filename}_angles.png'), temp_img)
    elif key == 32: # spacebar key
        temp_img = img.copy()
    
cv.destroyAllWindows()
