"""
Setup.

Package Setup.
"""

from setuptools import find_packages
from setuptools import setup

setup(
    name="readmemaker",
    version="2.0.0",
    description="Automate the process of generating a README.md",
    author="Contributors",
    url=("https://github.com/mrgrumpyowl/ai-tools.git"),
    py_modules=["readmemaker"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    install_requires=[
      "openai",
    ],
    entry_points={
        "console_scripts": [
            "readmemaker = readmemaker:main",
        ],
    },
)
