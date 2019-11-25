import argparse
import cv2

# construct the argument parse and parse the arguments
from Bills import Bills

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to the doc image")
ap.add_argument("-o", "--output", required=True,
                help="output doc file to writee")
ap.add_argument("-t", "--transformation", required=False,
                help="specify which transformation 1=Rotate, 2=Translate")
ap.add_argument("-p", "--rotate", required=False,
                help="specify transformation parameter, for e.g. -p 90 for 90 degrees")

args = vars(ap.parse_args())
input_doc_path = args["image"]
output_doc_path = args["output"]

if 'transformation' in args and 'rotate' in args:
    which_transform = args['transformation']
    rotate_angle = args['rotate']
    transform_param = dict()
    transform_param['angle'] = rotate_angle
    bill = Bills(input_doc_path)
    bill.transform_doc(which_transform, transform_param)
    bill.write_doc(output_doc_path)

