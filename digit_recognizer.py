import os
import numpy as np
import cv2
import torch
import pytesseract
root = os.getcwd()
sudoku_board = []

def getNumber(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Otsu Tresholding automatically find best threshold value
    _, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    # invert the image if the text is white and background is black
    count_white = np.sum(binary_image > 0)
    count_black = np.sum(binary_image == 0)
    if count_black > count_white:
        binary_image = 255 - binary_image
    # padding
    final_image = cv2.copyMakeBorder(image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    txt = pytesseract.image_to_string(
        final_image, config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
    return txt

print("-- Check the predicted numbers with the numbers in the sudoku grid \n Press Y or y if you want to change the number of just press Enter\n")
def digit_recognizer():
    for i,img_name in enumerate(sorted(os.listdir(os.path.join(root, 'temp')))):
        if '.png' not in img_name:
            continue
        img_path = os.path.join(root, 'temp', img_name)
#        print(img_path.split('/')[-1])
        row,col = i//9 + 1, i%9 + 1
        print(str(row) + ' x ' + str(col), sep = ' : ')
        
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        number = getNumber(cv2.imread(img_path)).replace('\x0c', '').strip()
        if np.all(img==0) or number not in list(map(str, range(0,10))):
            result = "."
        else:
            result = int(number)
        print(result)
        flag = input('Do you want to change the number ? (Y/N) :')
        if flag == 'y' or flag == 'Y':
            result = int(input("Enter the number :"))
            
        sudoku_board.append(result)
        
    return sudoku_board
