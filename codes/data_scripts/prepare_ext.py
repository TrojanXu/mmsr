import glob
import os
import argparse
import shutil
def move_files(src_list, png_desc, jpg_desc):
    if not os.path.exists(png_desc):
        os.makedirs(png_desc)
    if not os.path.exists(jpg_desc):
        os.makedirs(jpg_desc)

    files = []
    for src_path in src_list:
        files += glob.glob(src_path)
    for idx, img_path in enumerate(files):
        print('processing ' + img_path)
        if 'jpg' in img_path or 'jpeg' in img_path:
            #os.system('mv ' + img_path + ' ' + jpg_desc + '/{}.jpg'.format(idx))
            shutil.copy(img_path, jpg_desc+'/{}.jpg'.format(idx))
        elif 'png' in img_path:
            shutil.copy(img_path, png_desc+'/{}.png'.format(idx))
            #os.system('mv ' + img_path + ' ' + png_desc + '/{}.png'.format(idx))
        else:
            print(img_path + ' is not a valid image')

    print('done processing {} images'.format(len(files)))

if __name__ == '__main__':
    src_list = ['./2000-4K-Wallpapers-Themefoxx/*.jpg', './DIV2K_train_HR/*.png', './bjtu_wallpaper/*.jpg', './bjtu_wallpaper/*/*.jpg', './kaggle/*/dataraw/hires/*.jpg']
    move_files(src_list, './HR', './HR')