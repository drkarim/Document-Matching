'''
    Test Stub for Detecting Lines in Document

    Author: Rashed Karim
    Year: 2019

'''

import argparse
import os

import cv2
import re

# construct the argument parse and parse the arguments
from Bills import Bills


# https://stackoverflow.com/questions/37487758/how-to-add-an-id-to-filename-before-extension
def append_str_to_filename(filename, str_append):
    name, ext = os.path.splitext(filename)
    return "{name}_{uid}{ext}".format(name=name, uid=str_append, ext=ext)

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to the doc image")
ap.add_argument("-o", "--output", required=True,
                help="output doc file to writee")
#ap.add_argument('--batch', type=parseNumList, required=False, help='Perform multiple different rotations in a range')

args = vars(ap.parse_args())
input_doc_path = args["image"]
output_doc_path = args["output"]

bill = Bills(input_doc_path)

line_img = bill.detect_lines(0)
cv2.imshow("Detected lines in red", line_img)

bill.write_doc('line_detect', append_str_to_filename(output_doc_path, 'line_detect'))


