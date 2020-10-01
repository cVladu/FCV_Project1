import cv2
import os
from CONFIG import TEST, img_name_format
from FileHandler import get_all_images, read_config_file
from augmentations import apply_function

#TODO: Create git repository [SOLVED]

#TODO: Implement tkinter interface [SOLVED]

#TODO: Implement tint function [SOLVED]


def run_main(inp_dir, out_dir, config_file, index_start, recursive=False):
    if TEST:
        inp_dir = 'data/inp_dir'
        out_dir = 'data/out_dir'
        config_file = './config.txt'
        index_start = 1

    image_paths = get_all_images(inp_dir, recurse=recursive)
    transformations = read_config_file(config_file)
    images = [(cv2.imread(img_path), os.path.splitext(img_path)) for img_path in image_paths]

    index = index_start
    for func_dict in transformations:
        for img, (name_path, ext) in images:
            result_img = apply_function(img, func_dict['func'], **func_dict['params'])
            format_dict = {'name': os.path.split(name_path)[1],
                           'augmentation': func_dict['str_format'],
                           'index': index,
                           'ext': ext}
            cv2.imwrite(os.path.join(out_dir, img_name_format.format(**format_dict)), result_img)
            index += 1


if __name__ == '__main__':
    TEST = True
    run_main(*(None, None, None, None))