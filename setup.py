#!/usr/bin/env python
from setuptools import setup
import os


with open("./WazeRouteCalculator/__version__.py") as version_file:
    version = version_file.read().split("\"")[1]


def read(fname):
    try:
        with open(os.path.join(os.path.dirname(__file__), fname)) as f:
            return f.read()
    except IOError:
        return ""


setup(
    name = 'WazeRouteCalculator',
    version = version,
    author = 'Balint Kovacs',
    author_email = 'kovacsbalu@gmail.com',
    description = "Calculate actual route time and distance with waze api.",
    url = 'https://github.com/kovacsbalu/WazeRouteCalculator',
    download_url="https://github.com/kovacsbalu/WazeRouteCalculator/tarball/" + version,
    license = 'GNU GPL v3',
    keywords = ['waze', 'route', 'calculator'],
    packages = ['WazeRouteCalculator'],
    install_requires = ['requests'],
    long_description = read('readme.md')
)
