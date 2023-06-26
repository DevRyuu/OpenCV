# python 02_extract_pologon.py --input [image 폴더의 이미지 파일명] --color [배경의 색상]
# 4개의 점을 찍어 관심영역 다각형을 만든다
# ESC 배경이 제거된 이미지를 얻는다.

import cv2 as cv
import numpy as np
import argparse
import os

def draw_polygon(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            cv.circle(img, (x, y), 3, (0, 255, 0), -1)
            points.append((x, y))

        if len(points) == 4:
            image_polygon = img.copy()
            for point in points:
                cv.circle(image_polygon, point, 3, (0, 255, 0), -1)

            pts = np.array(points, np.int32)
            cv.polylines(image_polygon, [pts], True, (0, 255, 0), 2)
            cv.imshow("Image", image_polygon)

            mask = np.zeros_like(img)
            cv.fillPoly(mask, [pts], (255, 255, 255))
            image_mask = cv.bitwise_and(img, mask)
            cv.imshow("Masked Image", image_mask)          

            cv.imwrite(os.path.join(output_path, f"{input_filename}_polygon.png"), image_polygon)
            cv.imwrite(os.path.join(output_path, f"{input_filename}_polygon_mask_{color_bw}.png"), image_mask)            
            cv.waitKey(0)
            cv.destroyAllWindows()

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True, help="파일명")
parser.add_argument("--color", choices=["white", "black"], default="black", help="다각형 외부 색상")
args = parser.parse_args()

input_file = args.input
color_bw = args.color

input_filename, extension = input_file.split('.')
output_path = "result"

# 색상 옵션
if color_bw == "white":
    color = (255, 255, 255)
    mask_value = 255
else:
    color = (0, 0, 0)
    mask_value = 0

img = cv.imread(os.path.join(output_path, input_file), cv.IMREAD_COLOR)

points = []

cv.namedWindow("Image")
cv.setMouseCallback("Image", draw_polygon)

while True:
    cv.imshow("Image", img)
    if cv.waitKey(1) == 13: # ESC 키
        break

cv.destroyAllWindows()
