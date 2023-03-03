#!/usr/bin/env python
import sys

from setuptools import setup

__author__ = "Gavin Huttley"
__copyright__ = "Copyright 2019, Gavin Huttley"
__credits__ = ["Gavin Huttley"]
__license__ = "BSD"
__version__ = "0.1"
__maintainer__ = "Gavin Huttley"
__email__ = "Gavin.Huttley@anu.edu.au"
__status__ = "Alpha"

# Check Python version, no point installing if unsupported version inplace
if sys.version_info < (3, 7):
    py_version = ".".join([str(n) for n in sys.version_info])
    raise RuntimeError(
        "Python-3.6 or greater is required, Python-%s used." % py_version
    )

short_description = "c3dev"

# This ends up displayed by the installer
long_description = (
    """c3dev
tools to assist in development of PyCogent3
Version %s.
"""
    % __version__
)

setup(
    name="c3dev",
    version=__version__,
    author="Gavin Huttley",
    author_email="gavin.huttley@anu.edu.au",
    description=short_description,
    long_description=long_description,
    platforms=["any"],
    license=__license__,
    keywords=[
        "biology",
        "genomics",
        "genetics",
        "statistics",
        "evolution",
        "bioinformatics",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
    ],
    packages=["c3dev"],
    install_requires=[
        "click",
        "scriv",
    ],
    entry_points={
        "console_scripts": [
            "cleanup=c3dev.cleanup:main",
            "update_version=c3dev.update_version:main",
            "check_test_inclusion=c3dev.included_tests:main",
            "check_test_integrity=c3dev.integrity_tests:main",
            "move_merc=c3dev.relocate_mercurial:main",
            "c3dev_config=c3dev.devconfig:main",
        ]
    },
)
