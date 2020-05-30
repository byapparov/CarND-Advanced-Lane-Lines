import numpy as np


def estimate_lane_curve_radius_m(lane_ids, height):

    ym_per_pix: float = 30 / 720  # meters per pixel in y dimension
    xm_per_pix: float = 3.7 / 1000  # meters per pixel in x dimension

    x, y = zip(*lane_ids)

    fit = np.polyfit(np.asarray(y) * ym_per_pix, np.asarray(x) * xm_per_pix, 2)
    y = height * ym_per_pix

    a = fit[0]
    b = fit[1]
    c = fit[2]
    curve_radius = (1 + (2 * a * y + b) ** 2) ** (3 / 2) / abs(2 * a)

    return curve_radius
