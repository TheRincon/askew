from image_transformer import ImageTransformer
from util import save_image
import sys
import os
import subprocess
import argparse
import numpy as np

parser = argparse.ArgumentParser(
    description='Python3 Image Transformer',
    usage="askew.py [-i image_path] [-o outout] [--mode] [--theta] [--phi] [--gamma] [--height] [--width] [--dx] [--dy] [--dz]")
parser.add_argument('-i', dest="image_path", action="store", metavar='image_path',
                    type=str, help="input image path", required=True)
parser.add_argument('--mode', dest="mode", metavar='mode',
                    type=str, help="what command will generate (single image type or gif)", required=True)
parser.add_argument('-o', dest="output", metavar='output', action="store", type=str,
                    help='output dir or single image', default='output')
parser.add_argument('--theta', metavar='theta', type=int,
                    help='rotation around the x-axis', default=0)
parser.add_argument('--phi', metavar='phi', type=int,
                    help='rotation around the y-axis', default=0)
parser.add_argument('--gamma', metavar='gamma', type=int,
                    help='rotation around the z-axis ("normal" rotation)', default=0)
parser.add_argument('--height', metavar='height', type=int,
                    help='set height of output image', default=None)
parser.add_argument('--width', metavar='width', type=int,
                    help='set width of the output image', default=None)
parser.add_argument('--dx', metavar='dx', type=int,
                    help='pixel shift in the x direction', default=0)
parser.add_argument('--dy', metavar='dy', type=int,
                    help='pixel shift in the y direction', default=0)
parser.add_argument('--dz', metavar='dz', type=int,
                    help='pixel shift in the z direction (image distance)', default=0)
parser.add_argument('-j', help='make GIF of output', action='store_true')

options = parser.parse_args()

if options.image_path is None:
    raise ValueError('Image not found, check image path')

filename, file_extension = os.path.splitext(options.image_path)

it = ImageTransformer(options.image_path, height=options.height, width=options.width)

if not os.path.isdir('output'):
    os.mkdir('output')

if options.mode == 'single':
    rotated_img = it.rotate_along_axis(theta=options.theta, phi=options.phi, gamma=options.gamma, dx=options.dx, dy=options.dy, dz=options.dz)
    save_image(f'output/{options.output}{file_extension}', rotated_img)
elif options.mode == 'multi':
    rot_array = [rot for rot in [options.theta, options.phi, options.gamma, options.dx, options.dy, options.dz] if rot is not 0]
    if len(rot_array) == 0:
        raise ValueError('No rotations were set, please use command line flags -p, -t, -g, dx, dy, or dz and set at least one to an int')
    rot_range = max(rot_array) if max(rot_array) > 0 else 360
    for ang in range(0, rot_range):
        rotated_img = it.rotate_along_axis(
            theta=np.linspace(0,options.theta,rot_range, dtype = int)[ang],
            phi=np.linspace(0,options.phi,rot_range, dtype = int)[ang],
            gamma=np.linspace(0,options.gamma,rot_range, dtype = int)[ang],
            dx=np.linspace(0,options.dx,rot_range, dtype = int)[ang],
            dy=np.linspace(0,options.dy,rot_range, dtype = int)[ang],
            dz=np.linspace(0,options.dz,rot_range, dtype = int)[ang]
        )
        save_image('output/{}-{}.jpg'.format(options.output, str(ang)), rotated_img)
    if options.j:
        subprocess.run(["convert", f"output/{options.output}-%d{file_extension}[0-{rot_range - 1}]", f"example/{options.output}.gif"])
else:
    raise ValeuError('Mode not recognized')
