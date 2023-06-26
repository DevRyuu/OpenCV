import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
from matplotlib import font_manager, rc

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

# 명령행 인수 파싱
parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True, help="파일명")
parser.add_argument("--color", choices=["white", "black"], default="black", help="다각형 외부 색상")
args = parser.parse_args()

input_file = args.input
color_bw = args.color

input_filename, extension = input_file.split('.')
output_path = "result"

# 이미지 로드
img = cv.imread(os.path.join(output_path, input_file), cv.IMREAD_COLOR)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
mask = cv.imread(os.path.join(output_path, f"{input_filename}_polygon_mask_{color_bw}.png"), cv.IMREAD_COLOR)
mask_gray = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)

img_pixels = img.shape[0] * img.shape[1]
mask_pixels = mask.shape[0] * mask.shape[1]

mean_brightness_img = np.mean(img)
mean_brightness_mask = np.mean(mask)

print("원본 픽셀 개수:", img_pixels, "대상 픽셀 밝기 평균:", mean_brightness_img)
print("마스크 픽셀 개수:", mask_pixels, "마스크 픽셀 밝기 평균:", mean_brightness_mask)

cv.imwrite(os.path.join(output_path, f"{input_filename}_gray.png"), gray)
cv.imwrite(os.path.join(output_path, f"{input_filename}_mask_{color_bw}_gray.png"), mask_gray)

# 히스토그램 계산
hist = cv.calcHist([img], [0], None, [256], [1, 255])
hist2 = cv.calcHist([mask], [0], None, [256], [1, 255])

# 이진화
ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
ret2, thresh2 = cv.threshold(mask_gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)

cv.imwrite(os.path.join(output_path, f"{input_filename}_binary.png"), thresh)
cv.imwrite(os.path.join(output_path, f"{input_filename}_mask_{color_bw}_binary.png"), thresh2)

plt.close('all')
fig = plt.figure()

ax1 = plt.subplot(131)
ax1.plot(hist, color='b', label='글로벌')
ax1.plot(hist2, color='r', label='마스크')
ax1.legend()
ax1.set_xlim([0, 256])
ax1.set_title('밝기 히스토그램')

ax2 = plt.subplot(232)
ax2.imshow(img)
ax2.set_title('원본 영상')
ax2.axis('off')

ax3 = plt.subplot(233)
ax3.imshow(mask)
ax3.set_title('마스크 영상')
ax3.axis('off')

ax4 = plt.subplot(235)
ax4.imshow(thresh, cmap='gray')
ax4.set_title('글로벌 이진화')
ax4.axis('off')

ax5 = plt.subplot(236)
ax5.imshow(thresh2, cmap='gray')
ax5.set_title('마스크 이진화')
ax5.axis('off')

plt.tight_layout()
plt.savefig(os.path.join(output_path, f"{input_filename}_hist.jpg"))
plt.show()