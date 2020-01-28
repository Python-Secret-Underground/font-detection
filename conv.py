#!/usr/bin/env python3

# import concurrent.futures
import os
import subprocess
import sys
from typing import List, Tuple

import cv2
import numpy as np
from fontTools.ttLib import TTFont
from tqdm import tqdm


def make_font(fname: str) -> None:
    texts = 'texts'
    images = 'images'
    size = 200

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

    font = TTFont('../../' + fname)
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
    for filename in files:
        name, ext = os.path.splitext(filename)
        input_txt = texts + "/" + filename
        output_png = images + "/" + face + "_" + name + "_" + str(
            size) + ".png"

        subprocess.call([
            'convert', '-font', '../../' + fname, '-pointsize',
            str(size), 'label:@' + input_txt, output_png
        ])

    os.chdir(images)
    png = os.listdir()
    for i in png:
        if 'uni' in i or 'null' in i or 'space' in i:
            subprocess.call(['rm', i])

    out = np.zeros(cv2.imread(face + '_A_200.png').shape)
    # out = np.zeros((236, 129, 3))

    for i in os.listdir():
        img = cv2.imread(i)
        out = np.concatenate((out, img), axis=1)

    cv2.imwrite(face + '_out.png', out)
    os.chdir('../../')
    return fname


def main() -> None:
    # fname = 'ofl/anton/Anton-Regular.ttf'
    # fname = 'ofl/tangerine/Tangerine-Bold.ttf'

    fonts = [line.rstrip('\n') for line in open('fonts-list.txt')]

    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     res = [executor.submit(make_font, fname) for fname in fonts[:3]]

    # for i in res:
    #     print(i.result())
    try:
        os.mkdir('build')
        os.chdir('build')
    except FileExistsError:
        print('Please remove build/ directory')
        sys.exit(1)

    for fname in tqdm(fonts):
        make_font(fname)


if __name__ == '__main__':
    main()
