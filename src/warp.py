import cv2
import numpy as np
from numpy import single



class ImageWarp:

    def __init__(self, src, dst, height=720, width=1280):
        self.src_ = src
        self.dst_ = dst

        self.height = height
        self.width = width

        self.M_reverse = cv2.getPerspectiveTransform(dst, src)

    def top_view(self, img):
        M = cv2.getPerspectiveTransform(self.src_, self.dst_)
        return self.warp(img, M, 1.2)

    def car_view(self, img):
        M = cv2.getPerspectiveTransform(self.dst_, self.src_)
        return self.warp(img, M)

    def warp(self, img, M, width_scale = 1.0):
        """

        :type width_scale: float
        """
        return cv2.warpPerspective(
            img,
            M,
            (int(self.width * width_scale), self.height),
            flags=cv2.INTER_LINEAR
        )
