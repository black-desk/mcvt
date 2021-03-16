#!/usr/bin/env python3

from .types import *
import os, shutil, zipfile, tempfile
from defusedxml.ElementTree import parse
from bs4 import BeautifulSoup


def getIndex(id):
    if id == "Page_createby":
        return -1
    if id == "Page_cover":
        return 0
    if id.startswith("Page_"):
        return int(id[5:])
    return -1


def renameImgs(manifest, path):
    imgs = {}
    maxindex = 0
    for child in manifest:
        if child.attrib["id"].startswith("Page_"):
            index = getIndex(child.attrib["id"])
            maxindex = max(index, maxindex)
            html = os.path.join(path, child.attrib["href"])
            html = open(html, "r")
            html = html.read()
            html = BeautifulSoup(html, "html.parser")
            imgs[index] = os.path.join(path, html.img["src"][3:])
            if index == -1:
                os.remove(os.path.join(path, html.img["src"][3:]))
                continue
    for i in range(0, maxindex + 1):
        shutil.move(
            os.path.join(path, imgs[i]),
            os.path.join(os.path.join(path, "image"), "{:-05d}".format(i)) + ".jpg",
        )


def parseEpub(source: fileNameType,) -> str:
    tmpPath = tempfile.mkdtemp()

    epubFile = source[0] + "." + source[1]
    zipFile = os.path.join(tmpPath, os.path.basename(source[0]) + ".zip")

    shutil.copyfile(epubFile, zipFile)
    zipFile = zipfile.ZipFile(zipFile, "r")

    path = os.path.join(tmpPath, "extract")
    zipFile.extractall(path)

    # example:
    #
    # ❯ tree .                     # ❯ cat extract/html/99.html
    # .                            # <!DOCTYPE html SYSTEM "http://www.w~l.dtd">
    # ├── extract                  # <html xmlns="http://www.w~9/xhtml">
    # │   ├── css                  #   <head>
    # │   │   └── style.css        #     <title>第100页</title>
    # │   ├── html                 #     <link rel="stylesheet" type="text/css" href="../css/style.css"/>
    # │   │   ├── 100.html         #     <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    # │   │   ├── 101.html         #   </head>
    # │   │   ├── 102.html         #   <body>
    # │   │   ├── 103.html         #     <div class="fs">
    # │   │   ├── 104.html         #       <div>
    # │   │   ├── 105.html         #         <img src="../image/vol-005643.jpg" alt="Comic Book Images" class="singlePage" />
    # │   │   ├── 106.html         #       </div>
    # │   │   ├── 107.html         #     </div>
    # │   │   │ .................. #   </body>
    # │   │   ├── 93.html          # </html>
    # │   │   ├── 94.html          # ❯ cat extract/vol.opf
    # │   │   ├── 95.html          # <?xml version="1.0" encoding="UTF-8" ?>
    # │   │   ├── 96.html          #   <package version="2.0" unique-identifier="ISBN" xmlns="http://www.idpf.org/2007/opf">
    # │   │   ├── 97.html          #   <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
    # │   │   ├── 98.html          #     <dc:identifier id="ISBN" opf:scheme="ISBN">2001057010019</dc:identifier>
    # │   │   ├── 99.html          #     <dc:title>銀與金 - 第01卷</dc:title>
    # │   │   ├── 9.html           #     <dc:language>zh-CN</dc:language>
    # │   │   ├── cover.jpg.html   #     <dc:creator>福本伸行</dc:creator>
    # │   │   ├── cover.png.html   #     <dc:publisher>Vol.moe</dc:publisher>
    # │   │   ├── createby.html    #     <dc:date>2021</dc:date>
    # │   │   └── tpl_2.html       #     <dc:rights>Copyright © 2021 Vol.moe</dc:rights>
    # │   ├── image                #     <dc:series>銀與金</dc:series>
    # │   │   ├── cover.jpg        #     <meta name="cover" content="cover_img"/>
    # │   │   ├── createby.png     #   </metadata>
    # │   │   ├── vol-004955.jpg   #   <manifest>
    # │   │   ├── vol-005336.jpg   #     <item id="ncx" href="xml/vol.ncx" media-type="application/x-dtbncx+xml"/>
    # │   │   ├── vol-005643.jpg   #     <item id="Page_1" href="html/1.html" media-type="application/xhtml+xml"/>
    # │   │   ├── vol-006944.jpg   #     ...
    # │   │   ├── vol-014025.jpg   #     <item id="Page_198" href="html/198.html" media-type="application/xhtml+xml"/>
    # │   │   ├── vol-017641.jpg   #     <item id="Page_createby"  href="html/createby.html" media-type="application/xhtml+xml"/>
    # │   │   ├── vol-019990.jpg   #     <item id="Page_cover"     href="html/cover.jpg.html" media-type="application/xhtml+xml"/>
    # │   │   ├── vol-024141.jpg   #     <item id="cover_img" href="image/cover.jpg" media-type="image/jpeg" properties="cover-image" />
    # │   │   │ .................. #     <item id="img_1" href="image/vol-897208.jpg" media-type="image/jpeg"/>
    # │   │   ├── vol-860597.jpg   #     ...
    # │   │   ├── vol-866956.jpg   #     <item id="img_198" href="image/vol-733518.jpg" media-type="image/jpeg"/>
    # │   │   ├── vol-871086.jpg   #     <item id="img_createby" href="image/createby.png" media-type="image/png"/>
    # │   │   ├── vol-894192.jpg   #     <item id="css" href="css/style.css" media-type="text/css"/>
    # │   │   ├── vol-897208.jpg   #     <item id="font01" href="misc/Courier.ttf" media-type="application/x-font-ttf"/>
    # │   │   ├── vol-897729.jpg   #   </manifest>
    # │   │   ├── vol-898207.jpg   #   <spine toc="ncx">
    # │   │   └── vol-899201.jpg   #     <itemref idref="Page_cover" />
    # │   ├── META-INF             #     <itemref idref="Page_1" />
    # │   │   └── container.xml    #     ...
    # │   ├── mimetype             #     <itemref idref="Page_198" />
    # │   ├── misc                 #     <itemref idref="Page_createby" />
    # │   │   └── Courier.ttf      #   </spine>
    # │   ├── vol.opf              #   <guide>
    # │   └── xml                  #     <reference type="cover" href="image/cover.jpg" title="封面" />
    # │       └── vol.ncx          #   </guide>
    # └── source.zip               # </package>

    xmlfile = os.path.join(path, "META-INF", "container.xml")

    et = parse(xmlfile)
    root = et.getroot()
    xmlfile = os.path.join(path, root[0][0].attrib["full-path"])

    et = parse(xmlfile)
    root = et.getroot()

    manifest = root[1]
    renameImgs(manifest, path)

    # metadata = root[0]
    # metadata = readMetadata(metadata)

    return tmpPath


def parseZip(source: fileNameType) -> str:
    print("TODO")  # TODO
    return ""
