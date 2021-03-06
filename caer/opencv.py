#    _____           ______  _____ 
#  / ____/    /\    |  ____ |  __ \
# | |        /  \   | |__   | |__) | Caer - Modern Computer Vision
# | |       / /\ \  |  __|  |  _  /  Languages: Python, C, C++
# | |___   / ____ \ | |____ | | \ \  http://github.com/jasmcaus/caer
#  \_____\/_/    \_ \______ |_|  \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020 The Caer Authors <http://github.com/jasmcaus>


import cv2 as cv
import numpy as np
from urllib.request import urlopen

from .utilities import median, asarray
from .globals import (
    BGR2GRAY, BGR2RGB, BGR2HSV, BGR2LAB, RGB2BGR, RGB2GRAY, RGB2HSV, RGB2LAB, IMREAD_COLOR
)


__all__ = [
    'get_opencv_version',
    'mean',
    'merge',
    'split',
    'bgr_to_gray',
    'bgr_to_hsv',
    'bgr_to_lab',
    'bgr_to_rgb',
    'rgb_to_gray',
    'rgb_to_hsv',
    'rgb_to_lab',
    'rgb_to_bgr',
    'url_to_image',
    'color_map',
    'energy_map',
    'translate',
    'rotate',
    'edges'
]


def get_opencv_version():
    return cv.__version__[0]


def translate(image, x, y):
    """
        Translates a given image across the x-axis and the y-axis
        :param x: shifts the image right (positive) or left (negative)
        :param y: shifts the image down (positive) or up (negative)
    """
    transMat = np.float32([[1, 0, x], [0, 1, y]])
    return cv.warpAffine(image, transMat, (image.shape[1], image.shape[0]))


def rotate(image, angle, rotPoint=None):
    """
        Rotates an given image by an angle around a particular rotation point (if provided) or centre otherwise.
    """
    # h, w = image.shape[:2]
    # (cX, cY) = (w/2, h/2)

    # # Computing the sine and cosine (rotation components of the matrix)
    # transMat = cv.getRotationMatrix2D((cX, cY), angle, scale=1.0)
    # cos = np.abs(transMat[0, 0])
    # sin = np.abs(transMat[0, 1])

    # # compute the new bounding dimensions of the image
    # nW = int((h*sin) + (w*cos))
    # nH = int((h*cos) + (w*sin))

    # # Adjusts the rotation matrix to take into account translation
    # transMat[0, 2] += (nW/2) - cX
    # transMat[1, 2] += (nH/2) - cY

    # # Performs the actual rotation and returns the image
    # return cv.warpAffine(image, transMat, (nW, nH))

    height, width = image.shape[:2]

    # If no rotPoint is specified, we assume the rotation point to be around the centre
    if rotPoint is None:
        centre = (width//2, height//2)

    rotMat = cv.getRotationMatrix2D(centre, angle, scale=1.0)
    return cv.warpAffine(image, rotMat, (width, height))


# def rotate(img, angle):
#     h, w = img.shape[:2]
#     (cX, cY) = (w/2, h/2)

#     # Computing the sine and cosine (rotation components of the matrix)
#     transMat = cv.getRotationMatrix2D((cX, cY), angle, scale=1.0)
#     cos = np.abs(transMat[0, 0])
#     sin = np.abs(transMat[0, 1])

#     # compute the new bounding dimensions of the image
#     nW = int((h*sin) + (w*cos))
#     nH = int((h*cos) + (w*sin))

#     # Adjusts the rotation matrix to take into account translation
#     transMat[0, 2] += (nW/2) - cX
#     transMat[1, 2] += (nH/2) - cY

#     # Performs the actual rotation and returns the image
#     return cv.warpAffine(img, transMat, (nW, nH))


def edges(img, threshold1=None, threshold2=None, use_median=True, sigma=None):
    if not isinstance(use_median, bool):
        raise ValueError('use_median must be a boolean')

    if not isinstance(threshold1, int) or not isinstance(threshold2, int):
        raise ValueError('Threshold values must be integers')

    if img is None:
        raise ValueError('Image is of NoneType()')

    if not use_median and (threshold1 is None or threshold2 is None):
        raise ValueError('Specify valid threshold values')
    
    if use_median:
        if sigma is None:
            sigma = .3

        # computes the median of the single channel pixel intensities
        med = median(img)

        # Canny edge detection using the computed mean
        low = int(max(0, (1.0-sigma) * med))
        up = int(min(255, (1.0+sigma) * med))
        canny_edges = cv.Canny(img, low, up)
    
    else:
        canny_edges = cv.Canny(img, threshold1, threshold2)

    return canny_edges


def mean(image, mask=None):
    try:
        return cv.mean(image, mask=mask)
    except:
        raise ValueError('mean() expects an image')


def merge(img):
    # if not isinstance(img, (list, np.ndarray)):
    #     raise ValueError('img must be a list or numpy.ndarray of (ideally) shape = 3)')

    return cv.merge(img)


def split(img):
    try:
        return cv.split(img)
    except:
        raise ValueError('mean() expects an image')

    
def bgr_to_rgb(img):
    """
        Converts a BGR image to its RGB version
    """
    if len(img.shape) != 3:
        raise ValueError(f'Image of shape 3 expected. Found shape {len(img.shape)}. This method converts a BGR image to its RGB counterpart')

    return cv.cvtColor(img, BGR2RGB)


def rgb_to_bgr(img):
    """
        Converts an RGB image to its BGR version
    """
    if len(img.shape) != 3:
        raise ValueError(f'Image of shape 3 expected. Found shape {len(img.shape)}. This method converts an RGB image to its BGR counterpart')

    return cv.cvtColor(img, RGB2BGR)


def bgr_to_gray(img):
    """
        Converts a BGR image to its Grayscale version
    """
    if len(img.shape) != 3:
        raise ValueError(f'Image of shape 3 expected. Found shape {len(img.shape)}. This method converts a BGR image to its Grayscale counterpart')
    
    return cv.cvtColor(img, BGR2GRAY)


def rgb_to_gray(img):
    """
        Converts an RGB image to its Grayscale version
    """
    if len(img.shape) != 3:
        raise ValueError(f'Image of shape 3 expected. Found shape {len(img.shape)}. This method converts an RGB image to its Grayscale counterpart')
    
    return cv.cvtColor(img, RGB2GRAY)


def bgr_to_hsv(img):
    """
        Converts a BGR image to its HSV counterpart
    """
    if len(img.shape) != 3:
        raise ValueError(f'Image of shape 3 expected. Found shape {len(img.shape)}. This method converts a BGR image to its HSV counterpart')
    
    return cv.cvtColor(img, BGR2HSV)


def rgb_to_hsv(img):
    """
        Converts an RGB image to its HSV counterpart
    """
    if len(img.shape) != 3:
        raise ValueError(f'Image of shape 3 expected. Found shape {len(img.shape)}. This method converts an RGB image to its HSV counterpart')
    
    return cv.cvtColor(img, RGB2HSV)


def bgr_to_lab(img):
    """
        Converts a BGR image to its LAB counterpart
    """
    if len(img.shape) != 3:
        raise ValueError(f'Image of shape 3 expected. Found shape {len(img.shape)}. This method converts a BGR image to its LAB counterpart')

    return cv.cvtColor(img, BGR2LAB)


def rgb_to_lab(img):
    """
        Converts an RGB image to its LAB counterpart
    """
    if len(img.shape) != 3:
        raise ValueError(f'Image of shape 3 expected. Found shape {len(img.shape)}. This method converts an RGB image to its LAB counterpart')

    return cv.cvtColor(img, RGB2LAB)


def energy_map(img):
    img = bgr_to_gray(img.astype(np.uint8))

    dx = cv.Sobel(img, cv.CV_16S, 1, 0, ksize=3)
    abs_x = cv.convertScaleAbs(dx)
    dy = cv.Sobel(img, cv.CV_16S, 0, 1, ksize=3)
    abs_y = cv.convertScaleAbs(dy)
    output = cv.addWeighted(abs_x, 0.5, abs_y, 0.5, 0)

    return output


def color_map(img):
    gray_img = bgr_to_gray(img) 

    heatmap = cv.applyColorMap(gray_img, 11)
    superimpose = cv.addWeighted(heatmap, 0.7, img, 0.3, 0)

    return superimpose


def url_to_image(url, rgb=False):
    # Converts the image to a Numpy array and reads it in OpenCV
    response = urlopen(url)
    image = asarray(bytearray(response.read()), dtype='uint8')
    image = cv.imdecode(image, IMREAD_COLOR)
    if rgb:
        image = bgr_to_rgb(image)
    return image


__all__ = [
    'get_opencv_version',
    'mean',
    'merge',
    'split',
    'bgr_to_gray',
    'bgr_to_hsv',
    'bgr_to_lab',
    'bgr_to_rgb',
    'rgb_to_gray',
    'rgb_to_hsv',
    'rgb_to_lab',
    'rgb_to_bgr',
    'url_to_image',
    'translate',
    'rotate',
    'edges'
]