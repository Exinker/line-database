from setuptools import setup, find_packages

from line_database import DESCRIPTION, VERSION, NAME, AUTHOR_NAME, AUTHOR_EMAIL


setup(
	# info
    name=NAME,
	description=DESCRIPTION,
	license='MIT',
    keywords=['spectroscopy', 'spectra emulation', 'spectral line', 'database'],

	# version
    version=VERSION,

	# author details
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,

	# setup directories
    packages=find_packages(),

	# setup data
    package_data = {
        '': ['*.mnd'],
    },

	# requires
    python_requires='>=3.10',

)
