# python 01_brightneess.py --input [img 폴더의 이미지 파일명]
# 객체에 다수의 점을 찍어 밝기값을 얻는다 -> b 키를 누르고 배경에 다수의 점을 찍어 밝기값을 얻는다
# ESC 키를 눌러 밝기정보를 비교한다

import cv2 as cv
import numpy as np
import os
import argparse
import csv

def mouse_callback(event, x, y, flags, param):
    global select_object, object_points, background_points

    if event == cv.EVENT_LBUTTONDOWN:
        if select_object:
            object_points.append((x, y))
            cv.circle(img, (x, y), 3, (0, 0, 255), -1)
            brightness = gray[y, x]
            print(f"객체의 밝기 (x:{x}, y:{y}) = {brightness}")
        else:
            background_points.append((x, y))
            cv.circle(img, (x, y), 3, (255, 0, 0), -1)
            brightness = gray[y, x]
            print(f"배경의 밝기 (x:{x}, y:{y}) = {brightness}")
        cv.imshow("Brightness check", img)

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True, help="입력 파일명")
args = parser.parse_args()

input_file = args.input

input_filename, extension = input_file.split('.')
input_path = "image"
output_path = "result"
output_filename = os.path.join(output_path, input_filename)

img = cv.imread(os.path.join(input_path, input_file), cv.IMREAD_COLOR)
cv.imwrite(os.path.join(output_path, f"{input_filename}.png"), img)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

object_points = []      # 객체 포인트 리스트
background_points = []  # 배경 포인트 리스트
select_object = True    # 객체 선택 플래그

# 윈도우 및 마우스 콜백 설정
cv.namedWindow("Brightness check")
cv.setMouseCallback("Brightness check", mouse_callback)

while True:
    cv.imshow("Brightness check", img)
    key = cv.waitKey(1) & 0xFF

    if key == ord("b"):
        select_object = False
    elif key == 13:  # ESC키
        break

cv.destroyAllWindows()

object_points = np.array(object_points)
background_points = np.array(background_points)

max_points = max(object_points.shape[0], background_points.shape[0])
object_points = np.pad(object_points, ((0, max_points - object_points.shape[0]), (0, 0)), mode='constant')
background_points = np.pad(background_points, ((0, max_points - background_points.shape[0]), (0, 0)), mode='constant')

# 객체의 밝기 통계 계산
object_mean = np.mean(gray[object_points[:, 1], object_points[:, 0]])
object_min = np.min(gray[object_points[:, 1], object_points[:, 0]])
object_max = np.max(gray[object_points[:, 1], object_points[:, 0]])

# 배경의 밝기 통계 계산
background_mean = np.mean(gray[background_points[:, 1], background_points[:, 0]])
background_min = np.min(gray[background_points[:, 1], background_points[:, 0]])
background_max = np.max(gray[background_points[:, 1], background_points[:, 0]])

print(f"객체의 밝기 최대, 최소, 평균 = {object_max}, {object_min}, {object_mean}")
print(f"배경의 밝기 최대, 최소, 평균 = {background_max}, {background_min}, {background_mean}")

if object_mean > background_mean:
    print("[객체보다 어두운 배경입니다]")
else:
    print("[객체보다 밝은 배경입니다]")

object_brightness = gray[object_points[:, 1], object_points[:, 0]]
background_brightness = gray[background_points[:, 1], background_points[:, 0]]

# 밝기 정보를 CSV 파일로 저장
csv_data = np.column_stack((object_brightness, background_brightness))
csv_filename = f"{os.path.splitext(input_filename)[0]}_brightness.csv"
csv_path = os.path.join(output_path, csv_filename)

with open(csv_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["object_brightness", "background_brightness"])
    writer.writerows(csv_data)

print(f"{output_filename}.csv가 다음 경로에 저장되었습니다: {output_path}")
