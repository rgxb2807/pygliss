#!/usr/bin/env python3
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pygliss", 
    version="1.0.0",
    author="Ryan Beppel",
    author_email="ryan.beppel@gmail.com",
    description="Glissandi Relations Calculator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rgxb2807/pygliss",
    packages=setuptools.find_packages(),
    install_requires=[
          'numpy',
          'music21',
          'pygame',
          'scipy',
          'simpleaudio',
          'ipywidgets'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)