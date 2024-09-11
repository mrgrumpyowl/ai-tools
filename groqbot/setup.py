"""
Setup.

Package Setup.
"""

from setuptools import find_packages
from setuptools import setup

setup(
    name="groqbot",
    version="2.0.0",
    description="A chatbot powered by Mistral's Mixtral-8x7b model",
    author="Contributors",
    url=("https://github.com/mrgrumpyowl/ai-tools.git"),
    py_modules=["groqbot"],
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
      "groq",
      "prompt_toolkit",
      "rich",
      "tiktoken",
    ],
    entry_points={
        "console_scripts": [
            "groqbot = groqbot:main",
        ],
    },
)
