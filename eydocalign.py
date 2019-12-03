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
ap.add_argument("-s", "--source", required=True,
                help="path to the source doc image")
ap.add_argument("-t", "--target", required=True,
                help="path to the target doc image")
ap.add_argument("-o", "--output", required=True,
                help="output doc file to write")
#ap.add_argument('--batch', type=parseNumList, required=False, help='Perform multiple different rotations in a range')

args = vars(ap.parse_args())
source_doc_path = args["source"]
target_doc_path = args["target"]

output_doc_path = args["output"]

source_bill = Bills(source_doc_path)
target_bill = Bills(target_doc_path)

source_bill.align_orb(target_bill)

source_bill.write_doc('alignment', output_doc_path)
