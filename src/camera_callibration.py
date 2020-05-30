import glob
import numpy as np
import cv2

class CameraCalibrator:

    def __init__(self, images_path):


        self.images = glob.glob(images_path)

        self.board_size =  (9,6)


        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        self.objp = np.zeros((6 * 9, 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)


    def calibrate(self):
        objpoints = []
        imgpoints = []
        for fname in self.images:

            img = cv2.imread(fname)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Find the chessboard corners
            ret, corners = cv2.findChessboardCorners(gray, self.board_size, None)

            # If found, add object points, image points
            if ret == True:
                objpoints.append(self.objp)
                imgpoints.append(corners)

        # callibrate camera
        ret, self.mtx, self.dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)


    def undistort(self, img):
        return cv2.undistort(img, self.mtx, self.dist, None, self.mtx)