from typing import List, Any

import numpy as np
from numpy.core._multiarray_umath import ndarray


def smooth_array(x, N=50):
    smooth = np.convolve(x, np.ones((N,)) / N)[(N - 1):]
    smooth_shifted = np.zeros(N // 2)
    smooth_shifted = np.append(smooth_shifted, smooth[:len(x) - N // 2])
    return smooth_shifted


def weighted_lane_position(frequency):
    rates = []
    for i in range(len(frequency)):
        rates.append(i * frequency[i] / np.sum(frequency))
    return int(sum(rates))


def find_line_position(frequency, current, margin):
    """finds position of the lane using position of max value in the histogram."""

    width = len(frequency)
    if current + margin < width:
        window_right = current + margin
    else:
        print(
            "adjusting window - too high, current = {current}, margin = {margin}".format(current=current,
                                                                                         margin=margin))
        print("width {width}".format(width=width))
        window_right = width

    if current - margin > 0:
        window_left = current - margin
    else:
        print("adjusting window - too low")
        window_left = 0

    window = frequency[window_left: window_right]

    if len(window) > 0 and np.max(window) > 20:
        # threshold for max number of pixels in the window to change
        # position = window.argmax() + current - margin
        position = weighted_lane_position(window) + current - margin
    else:
        # don't change position as there are not enough points to move
        print("keeping current line position, max points is {points}".format(points=np.max(window)))
        position = current

    # here we can also add a check for number of

    return position


class TrafficLine:

    def __init__(self, side, margin=100, windows=10):
        # was the line detected in the last iteration?
        self.detected = False
        # x values of the last n fits of the line
        self.recent_xfitted = []
        # average x values of the fitted line over the last n iterations
        self.bestx = None
        # polynomial coefficients averaged over the last n iterations
        self.best_fit = None
        # polynomial coefficients for the most recent fit
        self.current_fit = [np.array([False])]
        # radius of curvature of the line in some units
        self.radius_of_curvature = None
        # distance in meters of vehicle center from the line
        self.line_base_pos = None
        # difference in fit coefficients between last and new fits
        self.diffs = np.array([0, 0, 0], dtype='float')
        # x values for detected line pixels
        self.allx = None
        # y values for detected line pixels
        self.margin = margin

        # number of windows to use in sliding window method
        self.windows = windows

        # array of (x, y) tuples
        self.line_indexes = []
        self.current = None

        # side of the line on the road: "left" or "right"
        self.side = side

    def init_position(self, img):
        height, width = img.shape

        if self.side == "left":
            self.current = self.init_position_left(img,  height // 2, height)
        else:
            # TODO: refactor hardcoded widths from original image
            self.current = self.init_position_right(img[:, :1280], height // 2, height) + 1280 // 2

    def init_position_left(self, img, ymin, ymax):
        """
        Finds initial position of the left lane
        :param img:
        :param ymin:
        :param ymax:
        :return:
        """
        height, width = img.shape
        frequency = np.sum(img[ymin:ymax, :width // 2], axis=0)
        hist_left_smooth: ndarray = smooth_array(frequency, 50)
        return hist_left_smooth.argmax()

    def init_position_right(self, img, ymin, ymax):
        """
        Finds initial position of the right lane (currently with half width offset)
        :param img:
        :param ymin:
        :param ymax:
        :return:
        """
        height, width = img.shape
        frequency = np.sum(img[ymin:ymax, width // 2:], axis=0)
        hist_left_smooth: ndarray = smooth_array(frequency, 50)
        return hist_left_smooth.argmax()

    def window_position_left(self, img, current, ymin, ymax):
        height, width = img.shape

        position = self.window_position(
            img[ymin:ymax, :width // 2],
            current,
        )
        return position

    def window_position_right(self, img, current, ymin, ymax):
        height, width = img.shape

        position = self.window_position(
            img[ymin:ymax, width // 2:],
            current - width // 2,  # adjust for crop on the right side
        )

        return position + width // 2

    def window_position(self, img, current):
        frequency = np.sum(img, axis=0)
        smooth = smooth_array(frequency, 10)
        position = find_line_position(
            frequency=smooth,
            current=current,
            margin=self.margin
        )
        return position

    def find_indexes(self, img):
        height, width = img.shape
        h = height // self.windows

        for window in range(self.windows):
            y_max: int = height - h * window
            y_min: int = height - h * (window + 1)
            y_position = (y_min + y_max) // 2

            if self.side == "left":
                x_position = self.window_position_left(
                    img,
                    self.current,
                    y_min,
                    y_max
                )
            else:
                x_position = self.window_position_right(
                    img,
                    self.current,
                    y_min,
                    y_max
                )
            self.current = x_position
            self.line_indexes.append((x_position, y_position))
