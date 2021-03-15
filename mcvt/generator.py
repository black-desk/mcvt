#!/usr/bin/env python3

import shutil, os
from .types import *
from PIL import Image


def genEpub(path: str) -> None:
    print("TODO")  # TODO
    return


def genZip(filename: str, path: str) -> None:

    l = os.listdir(path)

    ims = {}

    cnt = 1
    rate = 0

    for f in l:
        if f.endswith(".jpg") or f.endswith(".png"):
            im = Image.open(f)
            print(f)
            print(im.width, im.height)
            cnt += 1
            rate += im.width / im.height
            ims[f] = im

    rate /= cnt

    for f in ims:
        im = ims[f]
        r = im.width / im.height
        rr = im.height / 2 / im.width
        if (rate - r) ** 2 > (rate - rr) ** 2:
            filename = os.path.splitext(os.path.basename(f))[0]
            ext = os.path.splitext(os.path.basename(f))[1]
            im.show()
            s = input()
            if s == "y" or s == "Y":
                c1 = (0, 0, im.width, im.height / 2)
                c2 = (0, im.height / 2, im.width, im.height)
                im.crop(c1).rotate(270, expand=True).save(filename + "-1" + ext)
                im.crop(c2).rotate(270, expand=True).save(filename + "-2" + ext)
                os.remove(f)

    shutil.make_archive(filename, "zip", path)
    return
