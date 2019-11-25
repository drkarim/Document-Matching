import argparse
import cv2
import re

# construct the argument parse and parse the arguments
from Bills import Bills


def parseNumList(string):
    m = re.match(r'(\d+)(?:-(\d+))?$', string)
    # ^ (or use .split('-'). anyway you like.)
    if not m:
        raise ArgumentTypeError("'" + string + "' is not a range of number. Expected forms like '0-5' or '2'.")
    start = m.group(1)
    end = m.group(2) or start
    return list(range(int(start, 10), int(end, 10) + 1))


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to the doc image")
ap.add_argument("-o", "--output", required=True,
                help="output doc file to writee")
ap.add_argument("-t", "--transformation", required=False,
                help="specify which transformation 1=Rotate, 2=Translate")
ap.add_argument("-p", "--rotate", required=False,
                help="specify transformation parameter, for e.g. -p 90 for 90 degrees")
ap.add_argument('--batch', type=parseNumList, help='Perform multiple different rotations in a range')

args = vars(ap.parse_args())
input_doc_path = args["image"]
output_doc_path = args["output"]

if 'transformation' in args and 'rotate' in args:
    # Extract transformation params
    if args['transformation'] is not None and args['rotate'] is not None:
        which_transform = args['transformation']
        rotate_angle = args['rotate']
        transform_param = dict()
        transform_param['angle'] = rotate_angle

        # Execute
        bill = Bills(input_doc_path)
        bill.transform_doc(which_transform, transform_param)
        bill.write_doc('transform', output_doc_path)

# if 'batch' in args and 'angle_range' in args:
if 'batch' in args:
    angles = args['batch']

    bill = Bills(input_doc_path)
    bill.transform_doc_batch_angles(angles, output_doc_path)

