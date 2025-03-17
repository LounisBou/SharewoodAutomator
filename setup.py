#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sharewoodautomator",
    version="0.1.0",
    author="ShareWoodAutomator",
    author_email="lounis.bou@gmail.com",
    description="A Python library that automates interactions with ShareWood.tv",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LounisBou/sharewoodautomator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    install_requires=[
        "selenium>=4.0.0",
        "beautifulsoup4>=4.10.0",
        "python-dotenv>=0.19.0",
    ],
    keywords="sharewood, torrent, automation, scraper, downloader",
    project_urls={
        "Bug Reports": "https://github.com/LounisBou/sharewoodautomator/issues",
        "Source": "https://github.com/LounisBou/sharewoodautomator",
    },
)
