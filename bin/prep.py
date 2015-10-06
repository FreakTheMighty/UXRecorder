#!/bin/env python
import argparse
import os
import json
from PIL import Image, ImageDraw

if (__name__ == '__main__'):
    print('running')

    parser = argparse.ArgumentParser(description='Process image logs')
    parser.add_argument('--input', help='One or more images to prep for training data', nargs='+')
    parser.add_argument('--output', help='Output path to write processed data into')
    
    args = parser.parse_args()

    for img in args.input:

        jsonPath = img.replace('.jpg','.json')
        baseName = os.path.basename(img)

        if os.path.exists(jsonPath):
            with open(jsonPath) as jsonFile:
                jsonData = json.load(jsonFile)
                x = int(jsonData['mouseX']*256)
                y = int(jsonData['mouseY']*256)
                
                im = Image.open(img)

                resized = im.resize((256,256))
                resized.save(os.path.join(args.output, baseName), format="png")

                # Preview image
                draw = ImageDraw.Draw(resized)
                draw.arc([x-4, y-4, x+4, y+4], 0, 360, fill='magenta')
                del draw
                
                resized.save(os.path.join(args.output, baseName.replace('.jpg','-preview.jpg')), format="png")

                # Click output
                click = Image.new('L', (256,256))
                draw = ImageDraw.Draw(click)
                draw.point([x, y], fill='white')

                click.save(os.path.join(args.output, baseName.replace('.jpg','-target.jpg')), format="png")
