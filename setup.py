"""Setup configuration for OmniCamXploit."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="omnicamxploit",
    version="1.0.0",
    author="Md. Abu Naser Khan",
    description="Professional Camera Security Assessment Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joyelkhan/OmniCamXploit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "colorama>=0.4.6",
        "requests>=2.31.0",
        "tqdm>=4.66.0",
        "urllib3>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "omnicamxploit=omnicamxploit:main",
        ],
    },
)
