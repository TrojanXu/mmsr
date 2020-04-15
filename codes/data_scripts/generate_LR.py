import os
import glob
import cv2
import numpy as np


# we will not change HR image
# for LR image, if we provide png HR, we will add jpeg artifact to LR images as we would like to clean jpeg artifact
hr_path = './HR'
lr_x2_path = './LR_x2/'
lr_x4_path = './LR_x4/'

if not os.path.exists(lr_x2_path):
    os.makedirs(lr_x2_path)

if not os.path.exists(lr_x4_path):
    os.makedirs(lr_x4_path)

file_list = glob.glob(hr_path + '/*')

def save_image(path, img):
    if '.png' in path:
        cv2.imwrite(path, img)
    else:
        cv2.imwrite(path, img, [cv2.IMWRITE_JPEG_QUALITY, 100])

interp_mode = [cv2.INTER_AREA, cv2.INTER_NEAREST, cv2.INTER_LINEAR, cv2.INTER_CUBIC]
#interp_mode = [cv2.INTER_LINEAR, cv2.INTER_LINEAR, cv2.INTER_LINEAR, cv2.INTER_LINEAR]

scales = [2, 4]

count = 0
for file_path in file_list:
    img = cv2.imread(file_path)

    if img is None:
        print("error processing" + file_path)
        os.remove(file_path)
        continue
    if img.shape[0] < 480 or img.shape[1] < 480:
        print("image is not large enough" + file_path)
        os.remove(file_path)
        count = count+1        
        continue        

    _, fullfilename = os.path.split(file_path)
    filename, ext = os.path.splitext(fullfilename)

    if ext == 'png':
        #_, img = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), np.random.randint(50,100)])
        pass
    
    is_valid = True
    for scale in scales:
        if img.shape[0] % scale != 0 or img.shape[1] % scale != 0:
            print(file_path + "is not valid for scale {}.".format(scale))
            is_valid = False
            break

    if not is_valid:
        os.remove(file_path)
        count = count+1
        continue

    for scale in scales:
        if scale == 2:
            save_image(lr_x2_path+fullfilename, cv2.resize(img, (img.shape[1]//2, img.shape[0]//2), interpolation=interp_mode[np.random.randint(4)]))
        if scale == 4:
            save_image(lr_x4_path+fullfilename, cv2.resize(img, (img.shape[1]//4, img.shape[0]//4), interpolation=interp_mode[np.random.randint(4)]))



print('preprocessed {} images, {} failed for x2 or failed for x4'.format(len(file_list), count))