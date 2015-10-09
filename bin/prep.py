#!/bin/env python
import argparse
import os
import json
from PIL import Image, ImageDraw
from scipy import misc

import numpy as np

WIDTH = 512

def makeGaussian(size, fwhm = 3, center=None):
    """ Make a square gaussian kernel.
    size is the length of a side of the square
    fwhm is full-width-half-maximum, which
    can be thought of as an effective radius.
    """

    x = np.arange(0, size, 1, float)
    y = x[:,np.newaxis]
    
    if center is None:
        x0 = y0 = size // 2
    else:
        x0 = center[0]
        y0 = center[1]
    
    return np.exp(-4*np.log(2) * ((x-x0)**2 + (y-y0)**2) / fwhm**2)


if (__name__ == '__main__'):
    print('running')

    parser = argparse.ArgumentParser(description='Process image logs')
    parser.add_argument('--input', help='One or more images to prep for training data', nargs='+')
    parser.add_argument('--output', help='Output path to write processed data into')
    
    args = parser.parse_args()
    total = len(args.input)

    for idx, img in enumerate(args.input):

        jsonPath = img.replace('.jpg','.json')
        baseName = os.path.basename(img)

        if os.path.exists(jsonPath):
            print("Processing (%d of %d) %s ..." % (idx+1, total, img))
            with open(jsonPath) as jsonFile:
                jsonData = json.load(jsonFile)
                
                im = Image.open(img)

                x = int(jsonData['mouseX'] * WIDTH)
                y = int(jsonData['mouseY'] * WIDTH)

		print(x, y)
                resized = im.resize((WIDTH, WIDTH))
                resized.save(os.path.join(args.output, baseName.replace('.jpg','.png')), format="PNG")

                # Preview image
                draw = ImageDraw.Draw(resized)
                draw.arc([x-4, y-4, x+4, y+4], 0, 360, fill='magenta')
                del draw
                
                resized.save(os.path.join(args.output, baseName.replace('.jpg','-preview.png')), format="PNG")

                # Click output
                gauss = makeGaussian(WIDTH, WIDTH, (x, y))
		misc.imsave(os.path.join(args.output, baseName.replace('.jpg','-target.png')), gauss)
