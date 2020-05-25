import numpy as np
import cv2
import src.lib as lib


def apply_road_lane_binary_filter(img):
    s_grad_x_binary = apply_sobel_hsv(
        img,
        layer=1,  # saturation
        orient='x',
        thresh_min=20,
        thresh_max=100
    )

    r_grad_x_binary = apply_sobel(
        img,
        layer=2,  # red
        orient='x',
        thresh_min=20,
        thresh_max=100
    )

    s_binary_threshold = apply_absolute_threshold_hsv(
        img,
        layer=1,  # saturation
        thresh_min=220,
        thresh_max=250
    )

    r_binary_threshold = apply_absolute_threshold(
        img,
        layer=2,  # Red
        thresh_min=220,
        thresh_max=255
    )

    s_binary = cv2.bitwise_or(s_grad_x_binary, s_binary_threshold)
    r_binary = cv2.bitwise_or(r_grad_x_binary, r_binary_threshold)
    binary = cv2.bitwise_or(s_binary, r_binary)
    return binary


def apply_sobel_hsv(img, layer, orient='x', thresh_min=20, thresh_max=100):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    binary = apply_sobel(
        img=hsv,
        layer=layer,
        orient=orient,
        thresh_min=thresh_min,
        thresh_max=thresh_max
    )
    return binary


def apply_sobel(img, layer, orient='x', thresh_min=20, thresh_max=100):
    x = img[:, :, layer]
    binary = lib.abs_sobel_thresh(
        x,
        orient=orient,
        thresh_min=thresh_min,
        thresh_max=thresh_max
    )
    return binary


def apply_absolute_threshold_hsv(img, layer, thresh_min=200, thresh_max=255):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    binary = apply_absolute_threshold(
        hsv,
        layer=layer,
        thresh_min=thresh_min,
        thresh_max=thresh_max
    )
    return binary


def apply_absolute_threshold(img, layer, thresh_min=200, thresh_max=255):
    x = img[:, :, layer]
    binary = lib.abs_thresh(x, thresh_min=thresh_min, thresh_max=thresh_max)
    return binary
