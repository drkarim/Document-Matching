import imutils
import numpy as np
import pandas as pd
import cv2
import os
import random
import string



class Bills:
    image_transform = -1

    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        # load the image from disk
        self.image = cv2.imread(self.path_to_file)

    def transform_doc(self, which_transform, transform_param):

        if 'angle' in transform_param:
            angle = int(transform_param['angle'])

        elif 'gamma' in transform_param:
            gamma = int(transform_param['gamma'])

        if which_transform == 'rotate':
            self.image_transform = imutils.rotate(self.image, angle)

        elif which_transform == 'rotate_bound':
            self.image_transform = imutils.rotate_bound(self.image, angle)

        elif which_transform == 'gamma':
            self.image_transform = self.adjust_gamma(self.image, gamma)


    def write_doc(self, which_doc, write_path):
        if which_doc == 'transform':
            cv2.imwrite(write_path, self.image_transform)

    '''
        Rotates the document at multiple angles, and 
        writes each rotates image to file   
    '''
    def transform_doc_batch_angles(self,  angles, write_path):

        which_transform = 'rotate_bound'        # rotates without cutting the document
        transform_param = dict()
        transform_param['angle'] = 0
        # rotate doc at multiple angles and write to file
        for angle in angles:
            transform_param['angle'] = angle
            self.transform_doc('rotate_bound', transform_param)
            new_filename = self.append_num_to_filename(write_path, angle)
            self.write_doc('transform',  new_filename)

    # https://stackoverflow.com/questions/37487758/how-to-add-an-id-to-filename-before-extension
    def append_num_to_filename(self, filename, num):
        name, ext = os.path.splitext(filename)
        return "{name}_{uid}{ext}".format(name=name, uid=num, ext=ext)

    # https://stackoverflow.com/questions/33322488/how-to-change-image-illumination-in-opencv-python
    def adjust_gamma(self, image, gamma=1.0):

        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
                          for i in np.arange(0, 256)]).astype("uint8")

        return cv2.LUT(image, table)