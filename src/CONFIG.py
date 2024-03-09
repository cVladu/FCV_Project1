# -*- coding: utf-8 -*-

import augmentations

FUNC_MAPPING = {
    "rotate_image": augmentations.rotate_image,
    "rotate": augmentations.rotate_image,
    "tint_image": augmentations.tint_image,
    "tint": augmentations.tint_image,
    "hist": augmentations.hist,
    "histogram": augmentations.hist,
    "brightness": augmentations.increase_brightness,
    "bright": augmentations.increase_brightness,
    "modify_brightness": augmentations.increase_brightness,
    "increase_brightness": augmentations.increase_brightness,
    "contrast": augmentations.modify_contrast,
    "modify_contrast": augmentations.modify_contrast,
    "increase_contrast": augmentations.modify_contrast,
    "point_process": augmentations.linear_point_processing,
    "linear": augmentations.linear_point_processing,
    "point": augmentations.linear_point_processing,
    "gamma": augmentations.gamma_correction,
    "gamma_correction": augmentations.gamma_correction,
    "lut": augmentations.lookup_table,
    "lookup": augmentations.lookup_table,
    "lookup_table": augmentations.lookup_table,
    "equalize_hist": augmentations.hist_equalization,
    "eq_hist": augmentations.hist_equalization,
    "hist_eq": augmentations.hist_equalization,
    "hist_equalization": augmentations.hist_equalization,
    "dilate": augmentations.dilation,
    "dilation": augmentations.dilation,
    "erosion": augmentations.erosion,
    "erode": augmentations.erosion,
    "open": augmentations.opening,
    "opening": augmentations.opening,
    "close": augmentations.closing,
    "closing": augmentations.closing,
    "translate": augmentations.translation,
    "translation": augmentations.translation,
    "scale": augmentations.scale,
    "scaling": augmentations.scale,
}

TEST = False

img_name_format = "{name}_{augmentation}_{index}{ext}"
