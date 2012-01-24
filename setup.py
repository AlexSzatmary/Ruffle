#!/usr/bin/python

from ruffle import __version__

from setuptools import setup, find_packages
setup(
    name = "ruffle",
    version = __version__,
    packages = find_packages(),
    entry_points="""
    # -*- Entry points: -*-
    [console_scripts]
    ruffle=ruffle.ruffle:main
    """,
    author = "Alex C. Szatmary",
    author_email = "alex.szatmary@gmail.com",
    description = "Ruffle manages webs of citations in annotated "\
        "bibliographies",
    license = "MIT",
)
