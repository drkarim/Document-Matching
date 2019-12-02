'''
    Class Bill

    A Bill is a document scan of a bill or an invoice

    Author: Rashed Karim
    Year: 2019

'''

import imutils
import numpy as np
import pandas as pd
import cv2
import os
import math
import random
import string



class Bills:
    image_transform = -1

    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        # load the image from disk
        self.image = cv2.imread(self.path_to_file)
        self.line_image = self.image.copy()

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

        elif which_doc == 'line_detect':
            cv2.imwrite(write_path, self.line_image)

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

    '''
        Detect and draw lines  
    '''
    def detect_lines(self, only_lines=0):
        # https://stackoverflow.com/questions/45322630/how-to-detect-lines-in-opencv

        # Color to grey-level conversion
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        kernel_size = 5
        blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

        # Edge detection
        low_threshold = 50
        high_threshold = 150
        edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

        # Line detection
        rho = 1  # distance resolution in pixels of the Hough grid
        theta = np.pi / 180  # angular resolution in radians of the Hough grid
        threshold = 15  # minimum number of votes (intersections in Hough grid cell)
        min_line_length = 100  # minimum number of pixels making up a line
        max_line_gap = 20  # maximum gap in pixels between connectable line segments

        if only_lines == 1:
            self.line_image = np.copy(self.image) * 0  # creating a blank to draw lines on


        # Run Hough on edge detected image
        # Output "lines" is an array containing endpoints of detected line segments
        lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                                min_line_length, max_line_gap)

        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(self.line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)

        # Draw the lines on the  image
        lines_edges = cv2.addWeighted(self.image, 0.8, self.line_image, 1, 0)

        return self.line_image