import imutils
import numpy as np
import pandas as pd
import cv2


class Bills:
    image_transform = -1

    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        # load the image from disk
        self.image = cv2.imread(self.path_to_file)

    def transform_doc(self, which_transform, transfom_param):
        angle = transfom_param['angle']

        if which_transform == 'rotate':
            self.image_transform = imutils.rotate_bound(self.image, angle)

        elif which_transform == 'rotate_bound':
            self.image_transform = self.rotate_bound(self, angle)

    def rotate_bound(self, angle):
        # grab the dimensions of the image and then determine the
        # center
        (h, w) = self.image.shape[:2]
        (cX, cY) = (w // 2, h // 2)

        # grab the rotation matrix (applying the negative of the
        # angle to rotate clockwise), then grab the sine and cosine
        # (i.e., the rotation components of the matrix)
        M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])

        # compute the new bounding dimensions of the image
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))

        # adjust the rotation matrix to take into account translation
        M[0, 2] += (nW / 2) - cX
        M[1, 2] += (nH / 2) - cY

        # perform the actual rotation and return the image
        return cv2.warpAffine(self.image, M, (nW, nH))

    def write_doc(self, which_doc, write_path):
        if which_doc == 'transform':
            cv2.imwrite(write_path, self.image_transform)
