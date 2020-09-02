import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import shutil
import operator
import cv2
import image_slicer
from PIL import Image

root = os.getcwd()
def pre_process_image(img, skip_dilate=False):
    proc = cv2.GaussianBlur(img.copy(), (9, 9), 0)
    proc = cv2.adaptiveThreshold(proc, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    proc = cv2.bitwise_not(proc, proc)
    if not skip_dilate:
        kernel = np.ones((1,1),np.uint8)
        proc = cv2.dilate(proc, kernel)
    return proc

def find_corners_of_largest_polygon(img):
    """Finds the 4 extreme corners of the largest contour in the image."""
    contours, h = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Find contours
    contours = sorted(contours, key=cv2.contourArea, reverse=True)  # Sort by area, descending
    polygon = contours[0]  # Largest image
    bottom_right, _ = max(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    top_left, _ = min(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    bottom_left, _ = min(enumerate([pt[0][0] - pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    top_right, _ = max(enumerate([pt[0][0] - pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    return [polygon[top_left][0], polygon[top_right][0], polygon[bottom_right][0], polygon[bottom_left][0]]

def distance_between(p1, p2):
    """Returns the scalar distance between two points"""
    a = p2[0] - p1[0]
    b = p2[1] - p1[1]
    return np.sqrt((a ** 2) + (b ** 2))

def crop_and_warp(img, crop_rect):
    """Crops and warps a rectangular section from an image into a square of similar size."""
    top_left, top_right, bottom_right, bottom_left = crop_rect[0], crop_rect[1], crop_rect[2], crop_rect[3]
    src = np.array([top_left, top_right, bottom_right, bottom_left], dtype='float32')
    side = max([
        distance_between(bottom_right, top_right),
        distance_between(top_left, bottom_left),
        distance_between(bottom_right, bottom_left),
        distance_between(top_left, top_right)
    ])
    dst = np.array([[0, 0], [side - 1, 0], [side - 1, side - 1], [0, side - 1]], dtype='float32')
    m = cv2.getPerspectiveTransform(src, dst)
    return cv2.warpPerspective(img, m, (int(side), int(side)))

def infer_grid(img):
    """Infers 81 cell grid from a square image."""
    squares = []
    side = img.shape[:1]
    side = side[0] / 9
    for i in range(9):
        for j in range(9):
            p1 = (i * side, j * side)  # Top left corner of a bounding box
            p2 = ((i + 1) * side, (j + 1) * side)  # Bottom right corner of bounding box
            squares.append((p1, p2))
    return squares

def display_rects(in_img, rects, colour=255):
    """Displays rectangles on the image."""
    img = in_img.copy()
    for rect in rects:
        img = cv2.rectangle(img, tuple(int(x) for x in rect[0]), tuple(int(x) for x in rect[1]), colour)
    return img

def image_processor(img_path):
    image  = cv2.imread(img_path)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    ret, threshold1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    threshold2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    img = threshold2
    processed = img
    corners = find_corners_of_largest_polygon(processed)
    
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    corners = find_corners_of_largest_polygon(img)
    cropped = crop_and_warp(img, corners)
    squares = infer_grid(cropped)
    fin = []
    image = display_rects(cropped, squares)
    image = Image.fromarray(image)
    
    dir_name = 'temp'
    if dir_name in os.listdir():
        shutil.rmtree(dir_name)
    os.mkdir(dir_name)
    os.chdir(dir_name)
    image.save('my.png')
    a = image_slicer.slice('my.png', 81)
    
def black_white_converter(images):
    os.chdir(os.path.join(root, 'temp'))
    for img in images:
        if '.png' in img:
            image = cv2.imread(os.path.join(root, 'temp', img), cv2.IMREAD_GRAYSCALE)
            gray = cv2.resize(image, (256,256))
            result = gray[40:216, 40:216]
            ans = cv2.bitwise_not(result)
            ans1 = (ans//125)*255
            cv2.imwrite(img, ans1)

def main(img_path):
    image_processor(img_path)
    os.remove(os.path.join(os.getcwd(), 'my.png'))
    images = sorted(os.listdir())
    black_white_converter(images)
