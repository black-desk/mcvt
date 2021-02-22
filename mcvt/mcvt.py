#!/usr/bin/env python3

# Thanks https://docopt.org/
# Thanks https://wp-lai.gitbooks.io/learn-python/content/0MOOC/docopt.html

"""
mcvt - manga convertor

Usage:
  mcvt <source> <target>
  mcvt --version
  mcvt --help

Options:
  -h, --help                     Show this screen.
  --version                      Show version.
"""

from .types import *
from .docopt import docopt

import os

from .parser import *
from .generator import *


def convert(source: fileNameType, target: fileNameType) -> None:

    parseMethod = {"epub": parseEpub, "zip": parseZip}.get(source[1], None)
    assert parseMethod != None, f"unknown source format: {source[1]}"

    path = parseMethod(source)

    genMethod = {"epub": genEpub, "zip": genZip}.get(target[1], None)
    assert genMethod != None, f"unknown target format: {target[1]}"

    genMethod(target[0], os.path.join(os.path.join(path, "extract"), "image"))

    shutil.rmtree(path)
    return


def main():
    arguments = docopt(__doc__, version="mcvt 0.1")

    sourceFileName = os.path.abspath(arguments["<source>"])
    source = os.path.splitext(sourceFileName)
    source = source[0], source[1][1:]

    targetFileName = os.path.abspath(arguments["<target>"])
    target = os.path.splitext(targetFileName)
    target = target[0], target[1][1:]

    assert (
        source[1] != target[1]
    ), f"source format ({source[1]}) should different from target format ({target[1]}) "

    convert(source, target)
    return
