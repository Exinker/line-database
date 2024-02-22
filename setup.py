from setuptools import find_packages, setup

from spectrumlab_line_database import AUTHOR_EMAIL, AUTHOR_NAME, DESCRIPTION, NAME, VERSION


setup(
    # info
    name=NAME,
    description=DESCRIPTION,
    keywords=['spectroscopy', 'spectra emulation', 'spectral line', 'database'],
    version=VERSION,

    # license
    license='MIT',

    # author details
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,

    # setup directories
    packages=find_packages(),

    # setup data
    package_data={
        '': ['*.mnd'],
    },

    # requires
    install_requires=[
        item.strip() for item in open('requirements.txt', 'r').readlines()
        if item.strip()
    ],
    python_requires='>=3.10',

)
