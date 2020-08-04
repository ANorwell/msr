from setuptools import find_packages, setup
from msr.version import library_version

# Adapted from https://github.com/navdeep-G/setup.py/blob/master/setup.py


# Package meta-data.
NAME = 'msr'
DESCRIPTION = '.'
URL = 'https://github.com/me/myproject'
EMAIL = 'anorwell@gmail.com'
AUTHOR = 'Arron Norwell'
REQUIRES_PYTHON = '>=3.7.0'
VERSION = library_version()

# Required packages
REQUIRED = ['click', 'colorama']

# Optional packages
EXTRAS = {}


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],

    entry_points={
        'console_scripts': ['msr=msr.commands:cli'],
    },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT'
)