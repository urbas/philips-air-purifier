#!/usr/bin/env python

from setuptools import setup, find_packages

REQUIREMENTS = ["pycryptodome==3.9.0", "requests==2.22.0"]

SETUP_REQUIREMENTS = ["pytest-runner"]

TEST_REQUIREMENTS = ["pytest"]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    author_email="matej.urbas@gmail.com",
    author="Matej Urbas",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
    ],
    description="A Python API to monitor and control Philips air purifiers.",
    include_package_data=True,
    install_requires=REQUIREMENTS,
    keywords="philips-air-purifier",
    long_description_content_type="text/markdown",
    long_description=long_description,
    name="philips-air-purifier",
    packages=find_packages(include=["philips_air_purifier"]),
    setup_requires=SETUP_REQUIREMENTS,
    test_suite="tests",
    tests_require=TEST_REQUIREMENTS,
    url="https://github.com/urbas/philips-air-purifier",
    version="0.0.3",
)
