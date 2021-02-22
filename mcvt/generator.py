#!/usr/bin/env python3

import shutil
from .types import *


def genEpub(path: str) -> None:
    print("TODO")  # TODO
    return


def genZip(filename: str, path: str) -> None:
    shutil.make_archive(filename, "zip", path)
    return
