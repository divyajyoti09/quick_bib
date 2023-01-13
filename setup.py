#!/usr/bin/env python
"""
setup.py file for EccInspHMuSPA and EccInsp22uSPA pycbc waveform plugin package
"""

from setuptools import Extension, setup, Command
from setuptools import find_packages

VERSION = '1.0.dev0'

setup (
    name = 'quick_bib',
    version = VERSION,
    description = 'Package to create, edit, check for repeats, merge, and so on with bib files',
    author = 'Divyajyoti',
    author_email = 'divyajyoti.physics@gmail.com',
    download_url = '',
    keywords = ['tex', 'bib files'],
    install_requires = ['bibtexparser'],
    py_modules = ['quick_bib'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
)
