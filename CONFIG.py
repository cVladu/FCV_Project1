
from augmentations import *

FUNC_MAPPING = {
    'rotate_image': rotate_image,
    'rotate': rotate_image,
    'tint_image': tint_image,
    'tint': tint_image,
    'hist': hist,
    'histogram': hist,
    'brightness': increase_brightness,
    'bright': increase_brightness,
    'modify_brightness': increase_brightness,
    'increase_brightness': increase_brightness,
    'contrast': modify_contrast,
    'modify_contrast': modify_contrast,
    'increase_contrast': modify_contrast,
    'point_process': linear_point_processing,
    'linear': linear_point_processing,
    'point': linear_point_processing,
    'gamma': gamma_correction,
    'gamma_correction': gamma_correction,
    'lut': lookup_table,
    'lookup': lookup_table,
    'lookup_table': lookup_table,
    'equalize_hist': hist_equalization,
    'eq_hist': hist_equalization,
    'hist_eq': hist_equalization,
    'hist_equalization': hist_equalization,
    'dilate': dilation,
    'dilation': dilation,
    'erosion': erosion,
    'erode': erosion,
    'open': opening,
    'opening': opening,
    'close': closing,
    'closing': closing,
    'translate': translation,
    'translation': translation,
    'scale': scale,
    'scaling': scale,

}

TEST = False

img_name_format = '{name}_{augmentation}_{index}{ext}'

