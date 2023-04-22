"""
This module provides an OpenAlexWorks class. The class should have methods to get an RIS and a BibTeX entry for a DOI.
"""

from setuptools import setup

setup(
    name="s23openalex",
    version="0.0.1",
    description="OpenAlex utilities",
    long_description=__doc__,
    author="Yichen Zheng",
    author_email="yichenz3@andrew.cmu.edu",
    license="MIT",
    packages=["s23openalex"],
    python_requires=">=3.6",
)
