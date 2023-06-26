import cv2 as cv
import numpy as np
import os
import argparse

def on_trackbar(value):
    global gray, binary_img, adaptive_binary_mean, adaptive_binary_gaussian, block_size, sub_val
    
    ret, binary_img = cv.threshold(gray, value, 255, cv.THRESH_BINARY)
    adaptive_binary_mean = cv.adaptiveThreshold(binary_img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, block_size, sub_val)
    adaptive_binary_gaussian = cv.adaptiveThreshold(binary_img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, block_size, sub_val)
    ret2, binary_otsu = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    cv.putText(binary_otsu, f'threshold value: {ret}', org=(15, 20), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 255))

    cv.imshow('Binary', binary_img)
    cv.imshow('Adaptive Binary_mean', adaptive_binary_mean)
    cv.imshow('Adaptive Binary_gaussian', adaptive_binary_gaussian)
    cv.imshow('Otsu Binary', binary_otsu)

block_size = 3
sub_val = 2

parser = argparse.ArgumentParser(description='Binary thresholding test')
parser.add_argument('--input', required=True, help='Input image file path')
args = parser.parse_args() # args Namespace(input='test.jpg')

input_file = args.input # test.jpg
input_filename, extension = input_file.split('.') # test, jpg
input_path = 'image'
output_path = 'result'
output_file = os.path.join(output_path, f'{input_filename}.png') # result/test.png

img = cv.imread(os.path.join(input_path, input_file), cv.IMREAD_COLOR)
temp_img = img.copy()
gray = cv.cvtColor(temp_img, cv.COLOR_BGR2GRAY)

cv.namedWindow('Original')
cv.namedWindow('Grayscale')
cv.namedWindow('Binary')
cv.namedWindow('Adaptive Binary_mean')
cv.namedWindow('Adaptive Binary_gaussian')
cv.namedWindow('Otsu Binary')

cv.createTrackbar("Threshold", "Binary", 0, 255, on_trackbar)
cv.setTrackbarPos('Threshold', 'Binary', 127)

cv.createTrackbar("Block Size", "Adaptive Binary_mean", 3, 255, on_trackbar)
cv.createTrackbar("Subtract value", "Adaptive Binary_mean", 2, 255, on_trackbar)
cv.setTrackbarPos('Block Size', 'Adaptive Binary_mean', block_size)
cv.setTrackbarPos('Subtract value', 'Adaptive Binary_mean', sub_val)


while True:

    cv.imshow('Original', img)
    cv.imshow('Grayscale', gray)
    
    key = cv.waitKey(1) & 0xFF
    if key == 27: # esc key
        break
    elif key == 13: # enter key
        cv.imwrite(os.path.join(output_path, f'{input_filename}_binary.png'), binary_img)

cv.destroyAllWindows()
