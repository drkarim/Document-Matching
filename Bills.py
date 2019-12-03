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
        self.align_image = self.image.copy()

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

        elif which_doc == 'alignment':
            cv2.imwrite(write_path, self.align_image)

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


    ''' 
        Alignment of images using ORB features 
    '''
    def align_orb(self, target_bill):

        im1 = self.image
        im2 = target_bill.image

        MAX_FEATURES = 500
        GOOD_MATCH_PERCENT = 0.15

        # Convert images to grayscale
        im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
        im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

        # Detect ORB features and compute descriptors.
        orb = cv2.ORB_create(MAX_FEATURES)
        keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
        keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)

        # Match features.
        matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
        matches = matcher.match(descriptors1, descriptors2, None)

        # Sort matches by score
        matches.sort(key=lambda x: x.distance, reverse=False)

        # Remove not so good matches
        numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
        matches = matches[:numGoodMatches]

        # Draw top matches
        imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
        cv2.imwrite("matches.jpg", imMatches)

        # Extract location of good matches
        points1 = np.zeros((len(matches), 2), dtype=np.float32)
        points2 = np.zeros((len(matches), 2), dtype=np.float32)

        for i, match in enumerate(matches):
            points1[i, :] = keypoints1[match.queryIdx].pt
            points2[i, :] = keypoints2[match.trainIdx].pt

        # Find homography
        h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

        # Use homography
        height, width, channels = im2.shape
        im1Reg = cv2.warpPerspective(im1, h, (width, height))
        print("Estimated homography : \n", h)

        # compute angle from homography
        # https://answers.opencv.org/question/203890/how-to-find-rotation-angle-from-homography-matrix/
        if np.shape(h) == ():
            print("No transformation possible")
            return None, None

        ## derive rotation angle from homography
        theta = - math.atan2(h[0, 1], h[0, 0]) * 180 / math.pi
        print("Eatimated theta = ",theta)

        self.align_image = im1Reg
        #return im1Reg, h