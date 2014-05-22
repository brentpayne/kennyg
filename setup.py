#!/usr/bin/env python

from distutils.core import setup


def readme():
    try:
        import pypandoc
        description = pypandoc.convert('README.md', 'rst')
    except (IOError, ImportError, OSError):
        description = "Could not convert Markdown to reST\n" +\
            open('README.md').read()
    return description

setup(
    name='kennyg',
    version='0.1.4',
    description='KennyG SAX Handler',
    long_description=readme(),
    author='Brent Payne',
    author_email='brent.payne@gmail.com',
    url='http://www.github.com/brentpayne/kennyg',
    scripts=[
        'scripts/xml-tree.py',
    ],
    packages=[
        'kennyg',
    ],
    keywords=['sax', 'xml', 'kenny', 'parser'],
    classifiers=[
        "Topic :: Text Processing :: Markup :: XML",
        "Topic :: Text Processing :: General",
        "Topic :: Text Processing",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        ("License :: OSI Approved :: GNU Lesser General Public License v3" +
         " (LGPLv3)")
    ]

)
