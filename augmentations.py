import cv2
import numpy as np


def rotate_image(image, angle):
    """
    Rotate an image with the center pixel as the pivot.
    :param image: The image to rotate
    :param angle: The angle, in degrees
    :return: Rotated image in same format as the input image
    """
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def tint_image(image, channel, value):
    result = np.empty(image.shape, dtype=image.dtype)
    img_mask = np.zeros(image.shape, dtype=image.dtype)
    channel_index = 0 if channel == 'blue' else 1 if channel == 'green' else 2
    img_mask[:, :, channel_index] = np.iinfo(image.dtype).max
    beta = value/100.
    alpha = 1. - beta
    cv2.addWeighted(image, alpha, img_mask, beta, 0.0, result)
    return result


def apply_function(image, func, **kwargs):
    """
    Apply a transformation to the image
    :param image: The input image. The transformation / augmentation is applied to this image
    :param func: The transformation / augmentation to apply
    :param kwargs: Parameters for func
    :return: The resulting image, after the transformation / augmentation
    """
    return func(image, **kwargs)


def dummy_func(image, *args, **kwargs):
    """
    Dummy function
    :param image: Input image
    :param args: ...
    :return: ...
    """
    return image