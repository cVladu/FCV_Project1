import cv2
import matplotlib.pyplot as plt
import numpy as np
from functools import partial
import os


def _get_kernel(kernel=None, kernel_type=None, kernel_size=None):
    if kernel and not kernel_type and not kernel_size:
        if isinstance(kernel, list):
            kernel = np.array(kernel, dtype="uint8")
        else:
            raise Exception("kernel must be of type list")
    elif not kernel and kernel_type and kernel_size:
        rec_list = ["RECT", "RECTANGLE", "MORPH_RECT", "MORPH RECT"]
        ellipse_list = ["ELLIPSE", "ELL", "EL", "MORPH_ELLIPSE", "MORPH ELLIPSE"]
        cross_list = ["CROSS", "+", "MORPH_CROSS", "MORPH CROSS"]
        if kernel_type.upper() in rec_list:
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, tuple(kernel_size))
        elif kernel_type.upper() in ellipse_list:
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, tuple(kernel_size))
        elif kernel_type.upper() in cross_list:
            kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, tuple(kernel_size))
        else:
            raise Exception("kernel_type can onl be any of the following: {} or {} or {}".format(
                rec_list, ellipse_list, cross_list
            ))
    else:
        raise Exception("Either kernel or kernel_type and kernel_size must be given.")
    return kernel


def _get_min_max(image):
    min_value = np.iinfo(image.dtype).min
    max_value = np.iinfo(image.dtype).max
    return min_value, max_value


def rotate_image(image, angle):
    """
    Rotate an image with the center pixel as the pivot.
    :param image: The image to rotate
    :param angle: The angle, in degrees
    :return: Rotated image in same format as the input image
    """
    image = image.astype('uint8')
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def tint_image(image, value, channel=None, mask=None):
    result = np.empty(image.shape, dtype=image.dtype)
    img_mask = np.zeros(image.shape, dtype=image.dtype)
    if channel and not mask:
        channel_index = 0 if channel == 'blue' else 1 if channel == 'green' else 2 if channel == 'red' else None
        if not channel_index:
            raise Exception("Valid options for channel are: (blue, green, red)")
        img_mask[:, :, channel_index] = _get_min_max(image)[1]
    elif mask and not channel:
        img_mask[:, :] = mask
    else:
        raise Exception("Either channel or mask must be given.")
    beta = value/100. if value > 1 else value
    alpha = 1. - beta
    if alpha < 0 or alpha > 1:
        raise Exception("For tint_image, value must be between 0 and 100.")
    cv2.addWeighted(image, alpha, img_mask, beta, 0.0, result)
    return result


def hist(image, img_type="bgr"):
    calc_hist = partial(cv2.calcHist, images=[image], mask=None, histSize=[256], ranges=[0, 256])
    channel_color = zip([0, 1, 2], ('b', 'g', 'r')) if img_type.lower() == 'bgr' \
        else zip([0], ['k']) if img_type.lower() == 'gray' \
        else None
    if not channel_color:
        raise Exception("Argument img_type does not accept value {} for function hist".format(img_type))
    for channel, color in channel_color:
        hist_ = calc_hist(channels=[channel])
        plt.plot(hist_, color=color)
    plt.savefig('tmp.png')
    result = cv2.imread('tmp.png')
    os.remove('tmp.png')
    plt.clf()
    return result


def increase_brightness(image, beta):
    if beta < 0:
        raise Exception("For function increase_brightness, beta must be higher than 0.")
    result = linear_point_processing(image, beta=beta)
    return result


def modify_contrast(image, alpha):
    if 0 > alpha:
        raise Exception("For modify_contrast, alpha must be higher than 0 ")
    result = linear_point_processing(image, alpha=alpha)
    return result


def linear_point_processing(image, alpha=1, beta=0):
    min_value, max_value = _get_min_max(image)
    table = np.array([i * alpha + beta if i * alpha + beta < max_value else max_value
                      for i in np.arange(min_value, max_value + 1)]).astype(image.dtype)
    result = cv2.LUT(image, table)
    return result


def gamma_correction(image, gamma):
    min_value, max_value = _get_min_max(image)
    if gamma <= 0:
        raise Exception("For function gamma_correction, gamma must be higher than 0")
    inv_gamma = 1. / gamma
    table = np.array([((i / float(max_value)) ** inv_gamma) * max_value
                      for i in np.arange(min_value, max_value+1)]).astype(image.dtype)
    result = cv2.LUT(image, table)
    return result


def lookup_table(image, lut=None, blue=None, green=None, red=None):
    if lut and not blue and not green and not red:
        if len(lut) != 256:
            raise Exception("Provide a lookup table wih exactly 256 entries")
        lut = np.array(lut)
    elif not lut and blue and green and red:
        blue, green, red = np.array(blue), np.array(green), np.array(red)
        lut = np.dstack((blue, green, red))
        if lut.shape != (1, 256, 3):
            raise Exception("Provide a lookup table of 256 entries for each channel")
    else:
        raise Exception("Either lut or all blue, green, red parameters must be given.")
    image = image.astype('uint8')
    result = cv2.LUT(image, lut)
    return result


def hist_equalization(image, convert_to_gray=True, apply_to_rgb=False):
    if convert_to_gray:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        result = cv2.equalizeHist(image)
    elif not apply_to_rgb:
        img_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
        img_yuv[..., 0] = cv2.equalizeHist(img_yuv[..., 0])
        result = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    else:
        result = np.empty(image.shape, dtype=image.dtype)
        for channel in [0, 1, 2]:
            result[..., channel] = cv2.equalizeHist(image[..., channel])

    return result


def dilation(image, iterations, kernel=None, kernel_type=None, kernel_size=None, transform_binary=False):
    kernel = _get_kernel(kernel, kernel_type, kernel_size)
    if transform_binary:
        _, image = cv2.threshold(cv2.cvtColor(image, code=cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)
    result = cv2.dilate(image, kernel, iterations=iterations)
    return result


def erosion(image, iterations, kernel=None, kernel_type=None, kernel_size=None, transform_binary=False):
    kernel = _get_kernel(kernel, kernel_type, kernel_size)
    if transform_binary:
        _, image = cv2.threshold(cv2.cvtColor(image, code=cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)
    result = cv2.erode(image, kernel, iterations=iterations)
    return result


def opening(image, iterations, kernel=None, kernel_type=None, kernel_size=None, transform_binary=False):
    kernel = _get_kernel(kernel, kernel_type, kernel_size)
    if transform_binary:
        _, image = cv2.threshold(cv2.cvtColor(image, code=cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)
    result = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=iterations)
    return result


def closing(image, iterations, kernel=None, kernel_type=None, kernel_size=None, transform_binary=False):
    kernel = _get_kernel(kernel, kernel_type, kernel_size)
    if transform_binary:
        _, image = cv2.threshold(cv2.cvtColor(image, code=cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)
    result = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=iterations)
    return result


def translation(image, x_pixels, y_pixels):
    if -1. < x_pixels < 1.:
        x_pixels = image.shape[0] * x_pixels
    if -1. < y_pixels < 1.:
        y_pixels = image.shape[1] * y_pixels
    result = cv2.warpAffine(image, np.asarray([[1, 0, x_pixels], [0, 1, y_pixels]]), image.shape[1::-1])
    return result


def scale(image, x_factor, y_factor):
    result = cv2.warpAffine(image, np.asarray([[x_factor, 0, 0], [0, y_factor, 0]]),
                            (int(image.shape[1] * x_factor), int(image.shape[0] * y_factor)))
    return result


def dummy_func(image, *args, **kwargs):
    """
    Dummy function
    :param image: Input image
    :param args: ...
    :return: ...
    """
    return image


def apply_function(image, func, **kwargs):
    """
    Apply a transformation to the image
    :param image: The input image. The transformation / augmentation is applied to this image
    :param func: The transformation / augmentation to apply
    :param kwargs: Parameters for func
    :return: The resulting image, after the transformation / augmentation
    """
    return func(image, **kwargs)


def apply_chain(image, funcs, func_dicts):
    for func in funcs:
        func_dict = func_dicts[func]
        image = apply_function(image, func_dict['func'], **func_dict['params'])
    return image
