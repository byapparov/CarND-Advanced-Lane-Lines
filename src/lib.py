import numpy as np
import cv2

def abs_thresh(img, thresh_min=0, thresh_max=255):

    # Scale layer's values to 255
    img_int8 = np.uint8(255 / np.max(img) * img)

    binary_output = np.zeros_like(img_int8)
    binary_output[(img_int8 >= thresh_min) & (img_int8 <= thresh_max)] = 1
    return binary_output


def abs_sobel_thresh(img, orient='x', thresh_min=0, thresh_max=255):
    # Apply the following steps to img

    # Take the derivative in x or y given orient = 'x' or 'y'
    if orient == 'x':
        sobel = cv2.Sobel(img, cv2.CV_64F, 1, 0)
    if orient == 'y':
        sobel = cv2.Sobel(img, cv2.CV_64F, 0, 1)

    # Take the absolute value of the derivative or gradient
    abs_sobel = np.absolute(sobel)

    # Scale to 8-bit (0 - 255) then convert to type = np.uint8
    scaled_sobel = np.uint8(255 * abs_sobel / np.max(abs_sobel))

    # Create a mask of 1's where the scaled gradient magnitude
    # is > thresh_min and < thresh_max
    binary_output = np.zeros_like(scaled_sobel)
    binary_output[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1

    # 6) Return this mask as your binary_output image

    return binary_output
