# setup.py

from setuptools import setup, find_packages

setup(
    name="customControl4",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="An improved Python library for interacting with Control4 systems.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/customControl4",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.7.0",
        "async_timeout>=3.0.0",
        "python-socketio>=5.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Your License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
