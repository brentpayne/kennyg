#!/usr/bin/env python

from distutils.core import setup

readme = ""
with open('README.md', 'r') as fp:
    readme = ''.join(fp)

long_description = 'KennyG create a smooth and easy way to setup and parse' +\
    'SAX data.' + readme

setup(
    name='kennyg',
    version='0.1.4',
    description='KennyG SAX Handler',
    long_description=long_description,
    author='Brent Payne',
    author_email='brent.payne@gmail.com',
    url='http://www.github.com/brentpayne/kennyg',
    install_requires=[''],
    scripts=[
        'scripts/xml-tree.py',
    ],
    packages=[
        'kennyg',
    ],
    classifiers=[
        "Topic :: Text Processing :: Markup :: XML",
        "Topic :: Text Processing :: General",
        "Topic :: Text Processing",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)"
    ]

)
