"""
Setup.

Package Setup.
"""

from setuptools import find_packages
from setuptools import setup

print("Detected Packages:", find_packages())

setup(
    name="chatbot",
    version="2.0.0",
    description="An OpenAI powered chatbot",
    author="Contributors",
    url=("https://github.com/mrgrumpyowl/ai-tools.git"),
    py_modules=["chatbot", "model_config"],
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
      "requests",
      "tiktoken",
      "anthropic",
      "openai",
      "prompt_toolkit",
      "rich",
    ],
    entry_points={
        "console_scripts": [
            "chatbot = chatbot:main",
        ],
    },
)
