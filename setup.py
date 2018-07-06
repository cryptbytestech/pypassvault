# -*- coding: utf-8 -*-

# Setup for pypassvault project

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE.txt') as f:
    license = f.read()

setup(
    name='pypassvault',
    version='0.1.4',
    description='A simple commandline password vault written in python.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='cryptbytestech',
    author_email='cryptbytestech@gmail.com',
    url='https://github.com/cryptbytestech/pypassvault',
    #license=license,
    license="MIT",
    #packages=find_packages(exclude=('tests', 'docs'))
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        #'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],

    # What does your project relate to?
    keywords='password vault program cryptography',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'invoke>=0.19.0',
        'passlib>=1.7.1',
        'appdirs>=1.4.3',
        'cryptography>=1.8.1',
    ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
    #    'dev': [],
    #    'test': [],
    },
    entry_points = {
        'console_scripts': ['passvault=pypassvault.passvault:main'],
    },
)

