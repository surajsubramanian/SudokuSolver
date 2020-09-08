import os
import cv2
import csv
import pandas as pd
files = [i for i in os.listdir('images') if '.png' in i or '.jpg' in i]
label_df = pd.read_csv('labels.csv')
label_df['name'] = label_df['name'].astype(str)
label_df.set_index('name', inplace=True)

with open('content.csv', 'w') as f:
    writer = csv.writer(f)
    header = ['label']
    header += ['pixel'+str(i) for i in range(0, 784)]
    writer.writerow(header)
    for file in files:
        label = dict(label_df.loc[file])['label']
        image_path = os.path.join(os.getcwd(), 'images', file)
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (28,28)).reshape(1,784)
        l = img.tolist()[0]
        row = [label] + l
        writer.writerow(row)
