import os
import numpy as np
import cv2
import torch
import torch.nn as nn
from torchvision import transforms
from model import Net

root = os.getcwd()

model = Net()
model.load_state_dict(torch.load('mnist_weights.pth', map_location = torch.device('cpu')))
model.eval()
sudoku_board = []

def digit_recognizer():
    for img_name in sorted(os.listdir(os.path.join(root, 'temp'))):
        if '.png' not in img_name:
            continue
        img_path = os.path.join(root, 'temp', img_name)
        print(img_path)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (28,28))
        if np.all(img==0):
            result = "."
        else:
            img = torch.Tensor(img)
            x = img.unsqueeze(0).unsqueeze(0)
            output = model(x)
            pred = output.data.max(1, keepdim=True)[1]
            result = int(pred)
        sudoku_board.append(result)
        print(result)
        
    return sudoku_board
