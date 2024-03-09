# -*- coding: utf-8 -*-
import os

import cv2

from augmentations import apply_chain, apply_function
from CONFIG import TEST, img_name_format
from FileHandler import get_all_images, read_config_file


def run_main(inp_dir, out_dir, config_file, index_start, recursive=False):
    if TEST:
        inp_dir = "data/inp_dir"
        out_dir = "data/out_dir"
        config_file = "./config.yaml"
        index_start = 1

    image_paths = get_all_images(inp_dir, recurse=recursive)
    transformations, chain_transform = read_config_file(
        config_file, _type=os.path.splitext(config_file)[1]
    )
    images = [
        (cv2.imread(img_path), os.path.splitext(img_path))
        for img_path in image_paths  # noqa: E501
    ]

    index = index_start
    for transform in transformations.items():
        for img, (name_path, ext) in images:
            str_format, func_dict = transform[0], transform[1]
            try:
                enable = func_dict["en"]
            except KeyError:
                enable = True
            if enable:
                if not func_dict["params"]:
                    func_dict["params"] = {}
                result_img = apply_function(
                    img, func_dict["func"], **func_dict["params"]
                )
                format_dict = {
                    "name": os.path.split(name_path)[1],
                    "augmentation": str_format,
                    "index": index,
                    "ext": ext,
                }
                cv2.imwrite(
                    os.path.join(
                        out_dir, img_name_format.format(**format_dict)
                    ),  # noqa: E501
                    result_img,
                )
                index += 1
    if chain_transform:
        for img, (name_path, ext) in images:
            result_img = apply_chain(img, chain_transform, transformations)
            format_dict = {
                "name": os.path.split(name_path)[1],
                "augmentation": "Chain_" + "_".join(chain_transform),
                "index": index,
                "ext": ext,
            }
            cv2.imwrite(
                os.path.join(out_dir, img_name_format.format(**format_dict)),
                result_img,  # noqa: E501
            )
            index += 1


if __name__ == "__main__":
    run_main(*(None, None, None, None))
