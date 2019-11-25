import argparse
import os

import cv2
import re

# construct the argument parse and parse the arguments
from Bills import Bills


def parseNumList(string):
    m = re.match(r'(\d+)(?:-(\d+))?$', string)
    # ^ (or use .split('-'). anyway you like.)
    if not m:
        raise argparse.ArgumentTypeError("'" + string + "' is not a range of number. Expected forms like '0-5' or '2'.")
    start = m.group(1)
    end = m.group(2) or start
    return list(range(int(start, 10), int(end, 10) + 1))


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to the doc image")
ap.add_argument("-o", "--output", required=True,
                help="output doc file to writee")
ap.add_argument("-t", "--transformation", required=False,
                help="specify which transformation 1=Rotate, 2=Gamma illumination")
ap.add_argument("-p", "--amount", required=False,
                help="specify transformation parameter, for e.g. -p 90 for 90 degrees")
ap.add_argument('--batch', type=parseNumList, required=False, help='Perform multiple different rotations in a range')

args = vars(ap.parse_args())
input_doc_path = args["image"]
output_doc_path = args["output"]
bill = Bills(input_doc_path)


# https://stackoverflow.com/questions/37487758/how-to-add-an-id-to-filename-before-extension
def append_num_to_filename(filename, num):
    name, ext = os.path.splitext(filename)
    return "{name}_{uid}{ext}".format(name=name, uid=num, ext=ext)


if 'transformation' in args and 'amount' in args:
    # Extract transformation params
    if args['transformation'] is not None and args['amount'] is not None:
        which_transform = args['transformation']
        fn_append = 0           # what to append to filename to indicate the transformation, for example filename_0.png for 0 rotation

        if which_transform == 'rotate':
            rotate_angle = args['amount']
            transform_param = dict()
            transform_param['angle'] = rotate_angle
            fn_append = rotate_angle           # append to filename
        elif which_transform == 'gamma':
            gamma = args['amount']
            transform_param = dict()
            transform_param['gamma'] = gamma
            fn_append = gamma

        # Execute
        bill.transform_doc(which_transform, transform_param)
        bill.write_doc('transform', append_num_to_filename(output_doc_path, fn_append))


# if 'batch' in args and 'angle_range' in args:
elif 'batch' in args:
    angles = args['batch']

    bill = Bills(input_doc_path)
    bill.transform_doc_batch_angles(angles, output_doc_path)
