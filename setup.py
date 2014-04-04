#!/usr/bin/env python

from distutils.core import setup

setup(
    name='KennyG',
    version='0.1',
    description='KennyG SAX Handler',
    long_description=\
        'KennyG create a smooth and easy way to setup and parse SAX data.',
    author='Brent Payne',
    author_email='brent.payne@gmail.com',
    url='http://www.github.com/brentpayne/kennyg',
    install_requires=[''],
    scripts=[
        'scripts/xml-tree.py',
    ],
    packages=[
        'kennyg',
    ]
)
