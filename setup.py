# coding:utf8
from setuptools import setup

setup(
    name="mcvt",  # 应用名
    version="0.1",  # 版本号
    packages=["mcvt"],  # 包括在安装包内的Python包
    entry_points="""
    [console_scripts]
    mcvt = mcvt.mcvt:main
    """,
    install_requires=["defusedxml", "beautifulsoup4"],
)
