# 폴더[image]에 이미지 파일 넣고
# python 01_binary_test.py --input [파일명]
# python 01_binary_test.py --input test.jpg

import cv2 as cv
import numpy as np
import os
import argparse
import csv

def mouse(event, x, y, flags, param):
    pass

def calculate_brightness():
    pass

def save_brightness():
    pass

objects = []
backgrounds = []
select_object = True # 객체 선택 플래그




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="입력 파일명")
    args = parser.parse_args()