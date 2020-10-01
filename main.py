import cv2
import os
from CONFIG import TEST, img_name_format
from FileHandler import get_all_images, read_config_file
from augmentations import apply_function

#TODO: Create git repository
#TODO: Implement tkinter interface
#TODO: Implement tint function [SOLVED]

if __name__ == '__main__':
    if TEST:
        INP_DIR = 'data/inp_dir'
        OUT_DIR = 'data/out_dir'
        CONFIG_FILE = './config.txt'
        INDEX_START = 1

        image_paths = get_all_images(INP_DIR)
        transformations = read_config_file(CONFIG_FILE)
        images = [(cv2.imread(img_path), os.path.splitext(img_path)) for img_path in image_paths]

        index = INDEX_START
        for func_dict in transformations:
            for img, (name_path, ext) in images:
                result_img = apply_function(img, func_dict['func'], **func_dict['params'])
                format_dict = {'name': os.path.split(name_path)[1],
                               'augmentation': func_dict['str_format'],
                               'index': index,
                               'ext': ext}
                cv2.imwrite(os.path.join(OUT_DIR, img_name_format.format(**format_dict)), result_img)
                index += 1
