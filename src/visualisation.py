import numpy as np

def color_window_pixels(output, mask, corners, color = [(255, 0, 0)]):
    window = output[corners[0][1]:corners[1][1], corners[0][0]:corners[1][0]]
    window_warped = mask[corners[0][1]:corners[1][1], corners[0][0]:corners[1][0]]
    window[np.where(window_warped == [1])] = color

def window_corners(x, y, height, width):
    """
    Calculates bottom and top corner of the window

    :param x: middle of the window on X
    :param y: middle of the window on Y
    :param height: height of the window
    :param width: width of the window
    :return:
    """
    return [
        (int(x - width // 2), int(y - height // 2)),
        (int(x + width // 2), int(y + height // 2))
    ]
