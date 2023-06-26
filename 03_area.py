import cv2 as cv
import numpy as np
import os
import argparse



def calculate_perimeter(points):
    perimeter = 0
    for i in range(len(points)):
        perimeter += np.sqrt((points[i][0] - points[(i+1)%len(points)][0])**2 +
                             (points[i][1] - points[(i+1)%len(points)][1])**2)
    return perimeter

def calculate_area(points):
    area = 0
    for i in range(len(points)):
        area += (points[i][0] * points[(i+1)%len(points)][1]) - (points[i][1] * points[(i+1)%len(points)][0])
    area = abs(area) / 2
    return area

def draw_polygon(image, points):
    for i in range(len(points) - 1):
        cv.line(image, points[i], points[i+1], (0, 255, 0), 2)
    if len(points) > 2:
        cv.line(image, points[-1], points[0], (0, 255, 0), 2)

def mouse_callback(event, x, y, flags, param):
    global points, is_drawing

    if event == cv.EVENT_LBUTTONDOWN:
        if is_drawing:
            points.append((x, y))
            cv.circle(temp_img, (x, y), effect_radius, (255, 0, 0), -1)
            if len(points) > 1:
                cv.line(temp_img, points[-2], points[-1], (0, 0, 255), effect_thickness)
        if len(points) > 2 and np.linalg.norm(np.array(points[0]) - np.array((x, y))) < effect_radius:
            perimeter = calculate_perimeter(points)
            area = calculate_area(points)
            print("다각형 둘레:", perimeter)
            print("다각형 넓이:", area)
            cv.putText(temp_img, f"Perimeter: {perimeter:.3f}", (points[-1][0], points[-1][1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 204, 255), 2)
            cv.putText(temp_img, f"Area: {area:.3f}", (points[-1][0], points[-1][1]+20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 204, 255), 2)
            is_drawing = False

points = []
is_drawing = True
effect_radius = 4
effect_thickness = 2

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
    if is_drawing:
        drawing_image = temp_img.copy()
        text = 'Image initialize if press "Space bar" key'
        cv.putText(temp_img, text=text, org=(15, 20), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 255))
        draw_polygon(drawing_image, points)
        cv.imshow("Angle of 2 lines", drawing_image)
    else:
        cv.imshow("Angle of 2 lines", temp_img)
    
    key = cv.waitKey(1) & 0xFF
    if key == 27:  # ESC key
        break
    elif key == 13:
        cv.imwrite(os.path.join(output_path, f'{input_filename}_area.png'), temp_img)
    elif key == 32: # spacebar key
        points = []
        is_drawing = True
        temp_img = img.copy()

cv.destroyAllWindows()
