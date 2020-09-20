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
def imageProcessor(img_path):
    image  = cv2.imread(img_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
    contours,_ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return image, gray, thresh, contours

def bestContours(image, contours):
    max_area = 0
    c = 0
    for i in contours:
        area = cv2.contourArea(cv2.UMat(i))
        if area > 1000:
            if area > max_area:
                max_area = area
                best_cnt = i
        c+=1
    return best_cnt

def maskCreator(gray, best_cnt, image, contours):
    mask = np.zeros((gray.shape),np.uint8)
    cv2.drawContours(mask,[best_cnt],0,255,-1)
    cv2.drawContours(mask,[best_cnt],0,0,2)

    out = np.zeros_like(gray)
    out[mask == 255] = gray[mask == 255]
    blur = cv2.GaussianBlur(out, (11,11), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
    c = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 1000/2:
            cv2.drawContours(image, contours, c, (0, 255, 0), 3)
        c+=1
    return image,out

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

def boxFinder(image, out):
    final = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    contours, h = cv2.findContours(out.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    polygon = contours[0]

    bottom_right, _ = max(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    top_left, _ = min(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    bottom_left, _ = min(enumerate([pt[0][0] - pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    top_right, _ = max(enumerate([pt[0][0] - pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    box = [polygon[top_left][0], polygon[top_right][0], polygon[bottom_right][0], polygon[bottom_left][0]]

    gray = crop_and_warp(final, box)
    return gray

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
    

def main(img_path):
    image, gray, thresh, contours = imageProcessor(img_path)
    best_cnt = bestContours(image, contours)
    image,out = maskCreator(gray, best_cnt, image, contours)
    gray = boxFinder(image, out)
    
    squares = infer_grid(gray)
    image = display_rects(gray, squares)
    image1 = Image.fromarray(image)
    image1.save('my.png')
    a = image_slicer.slice('my.png', 81)

    if 'temp' in os.listdir():
        shutil.rmtree('temp')
    os.mkdir('temp')
    for i,img in enumerate(sorted([file for file in os.listdir() if 'my_' in file])):
        src, dst = os.path.join(root, img), os.path.join(root, 'temp')
        shutil.move(src, dst)

    for img_name in os.listdir('temp'):
        if '.png' in img_name:
            img = cv2.imread(os.path.join(root, 'temp', img_name))
            img[img > 50] = 255
            image_inverted = cv2.bitwise_not(img)
            cv2.imwrite(os.path.join(root, 'temp', img_name), image_inverted)

def sudoku_solver(img_path):
    main(img_path)
