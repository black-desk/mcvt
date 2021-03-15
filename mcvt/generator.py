#!/usr/bin/env python3

import shutil, os
from .types import *
from PIL import Image


def genEpub(path: str) -> None:
    print("TODO")  # TODO
    return


def genZip(fn: str, path: str) -> None:

    l = os.listdir(path)

    ims = {}
    S = {}

    cnt = 1
    rate = 0
    width = 0

    for f in l:
        if f.endswith(".jpg") or f.endswith(".png"):
            f = os.path.join(path, f)
            im = Image.open(f)
            cnt += 1
            rate += im.width / im.height
            ims[f] = im
            width += im.width

    rate /= cnt
    width /= cnt

    for f in ims:
        im = ims[f]
        r = im.width / im.height
        rr = im.height / 2 / im.width
        if (rate - r) ** 2 > (rate - rr) ** 2 and im.width > width:
            filename = os.path.splitext(os.path.basename(f))[0]
            filename = os.path.join(path, filename)
            ext = os.path.splitext(os.path.basename(f))[1]
            c1 = (0, 0, im.width, im.height / 2)
            c2 = (0, im.height / 2, im.width, im.height)
            im.crop(c1).rotate(270, expand=True).save(filename + "-1" + ext)
            im.crop(c2).rotate(270, expand=True).save(filename + "-2" + ext)
            os.remove(f)

    shutil.make_archive(fn, "zip", path)
    return
