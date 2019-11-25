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
        angle = int(transfom_param['angle'])

        if which_transform == 'rotate':
            self.image_transform = imutils.rotate(self.image, angle)

        elif which_transform == 'rotate_bound':
            self.image_transform = imutils.rotate_bound(self.image, angle)


    def write_doc(self, which_doc, write_path):
        if which_doc == 'transform':
            cv2.imwrite(write_path, self.image_transform)
