import cv2
import numpy as np


img = cv2.imread("./image/seed_01.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, binary_img = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(binary_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 객체들을 4행으로 정렬한다.
objects = []
for cnt in contours:
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    objects.append(box)

# 객체들을 정렬한다.
objects.sort(key=lambda x: x[0][1])

# 객체들을 이미지에 표시한다.
for obj in objects:
    cv2.drawContours(img, [obj], 0, (0, 255, 0), 2)

# 이미지를 저장한다.
cv2.imwrite("output.jpg", img)