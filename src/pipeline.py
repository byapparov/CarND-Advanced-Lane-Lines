from src.binary_lane_filter import apply_road_lane_binary_filter
import numpy as np
import cv2
from src.warp import ImageWarp
from src.line import TrafficLine
from src.visualisation import window_corners, color_window_pixels
from src.curvature import estimate_lane_curve_radius_m

from src.camera_callibration import CameraCalibrator

def create_image_processor():
    calibrator = CameraCalibrator('camera_cal/calibration*.jpg')
    calibrator.calibrate()

    def process_image(img):

        # calibrate image
        img = calibrator.undistort(img)

        # apply binary filter
        output_binary = apply_road_lane_binary_filter(img)

        # warp image
        src = np.float32([[500, 515], [760, 500], [200, 720], [1100, 720]])
        dst = np.float32([[200, 500], [1100, 500], [200, 700], [1110, 700]])

        warp = ImageWarp(src, dst)

        warped = warp.top_view(output_binary)

        # find lanes with sliding windows method
        margin = 100
        height, width, layers = img.shape
        h = height / 10  # windows

        out_img = cv2.merge([warped * 255, warped * 255, warped * 255])

        left_line = TrafficLine("left", margin=margin)
        left_line.init_position(warped)
        left_line.find_indexes(warped)

        right_line = TrafficLine("right", margin=margin)
        right_line.init_position(warped)
        right_line.find_indexes(warped)

        for x, y in left_line.line_indexes:
            corners = window_corners(x, y, h, margin * 2)
            color_window_pixels(out_img, warped, corners, [(0, 255, 0)])

            cv2.rectangle(
                out_img,
                corners[0],
                corners[1],
                color=(0, 0, 255),
                thickness=2
            )

        for x, y in right_line.line_indexes:
            corners = window_corners(x, y, h, margin * 2)
            color_window_pixels(out_img, warped, corners, [(255, 0, 0)])

            cv2.rectangle(
                out_img,
                corners[0],
                corners[1],
                color=(0, 0, 255),
                thickness=2
            )

        left_line_curvature = estimate_lane_curve_radius_m(left_line.line_indexes, height)
        right_line_curvature = estimate_lane_curve_radius_m(right_line.line_indexes, height)

        # Write curvature and car position text

        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        fontColor = (255, 255, 255)
        lineType = 2

        cv2.putText(
            img,
            "Radius of Curvature: {:.0f} meters".format(left_line_curvature // 2),
            (100, 50),
            font,
            fontScale,
            fontColor,
            lineType
        )

        # it looks like camera position on the car needs calibration
        # looking it test images, it seems that middle of the car is closer to 680px
        # as opposed to 640 expected
        mid_x = 680 # width // 2
        xm_per_pix: float = 3.7 / 1000

        car_position = ((left_line.line_indexes[0][0] + right_line.line_indexes[0][0]) / 2 - mid_x) * xm_per_pix

        if car_position > 0:
            position_side = "right"
        else:
            position_side = "left"
        cv2.putText(
            img,
            "Car position: {position_side} {car_position:.2f} meters".format(
                position_side=position_side,
                car_position=abs(car_position)
            ),
            (100, 100),
            font,
            fontScale,
            fontColor,
            lineType
        )

        # Restore the car view

        visual_output = warp.car_view(out_img)

        # Clean overlay visualisation from white dots
        lower_white = np.array([50, 50, 50], dtype="uint16")
        upper_white = np.array([255, 255, 255], dtype="uint16")
        white_mask = cv2.inRange(visual_output, lower_white, upper_white)
        visual_output[np.where((white_mask != [0]))] = [0, 0, 0]

        overlay_out = np.copy(img)
        visual_output_gray = cv2.cvtColor(visual_output, cv2.COLOR_BGR2GRAY)
        overlay_out[(visual_output_gray > 10)] = [0, 0, 0]
        overlay_out = cv2.addWeighted(overlay_out, 1, visual_output, 1, 0)

        return overlay_out

    return process_image