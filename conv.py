#!/usr/bin/env python3

import os
import subprocess
from typing import List, Tuple

import cv2
import numpy as np
from fontTools.ttLib import TTFont

from tqdm import tqdm


def main() -> None:
    # fname = 'ofl/anton/Anton-Regular.ttf'
    # fname = 'ofl/tangerine/Tangerine-Bold.ttf'
    texts = 'texts'
    images = 'images'
    size = 200

    fonts = [line.rstrip('\n') for line in open('fonts-list.txt')]
    print(fonts)

    for fname in fonts:
        face = fname.split('/')[-1].split('.')[0]

        try:
            os.mkdir(face)
            os.chdir(face)
        except FileExistsError:
            os.chdir(face)

        try:
            os.mkdir(images)
        except FileExistsError:
            pass

        try:
            os.mkdir(texts)
        except FileExistsError:
            pass

        font = TTFont('../' + fname)
        asc: List[Tuple[int, str]] = []

        for x in font['cmap'].tables:
            for y in x.cmap.items():
                if y[0] < 0x80:
                    asc.append(y)

        for i in asc:
            ucode = chr(i[0])
            utf8 = ucode.encode('utf-8')
            name = i[1]
            with open(os.path.join(texts, name + '.txt'), 'w') as f:
                f.write(utf8.decode('utf-8'))

        font.close()

        files = os.listdir(texts)
        for filename in tqdm(files):
            name, ext = os.path.splitext(filename)
            input_txt = texts + "/" + filename
            output_png = images + "/" + face + "_" + name + "_" + str(
                size) + ".png"

            subprocess.call([
                'convert', '-font', '../' + fname, '-pointsize',
                str(size), 'label:@' + input_txt, output_png
            ])

        os.chdir(images)
        png = os.listdir()
        for i in png:
            if 'uni' in i or 'null' in i or 'space' in i:
                subprocess.call(['rm', i])

        out = np.zeros(cv2.imread(face + '_A_200.png').shape)
        # out = np.zeros((236, 129, 3))
        print(out.shape)
        for i in os.listdir():
            img = cv2.imread(i)
            print(i)
            print(img.shape)
            out = np.concatenate((out, img), axis=1)

        cv2.imwrite(face + '_out.png', out)


if __name__ == '__main__':
    main()
