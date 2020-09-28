import io
import re

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# get version from package's __version__
__version__ = re.search(
        r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',  # It excludes inline comment too
        io.open('cartoons/__init__.py', encoding='utf_8_sig').read()
    ).group(1)

setuptools.setup(
    name="cartoonista",
    version=__version__,
    author="Robert Lieback",
    author_email="robertlieback@zetabyte.de",
    description="A library to get a random cartoon image url from 11000+ cartoons. "
                "It also contains the scrapers for many cartoon websites.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Netzvamp/cartoonista",
    project_urls={
        "Documentation": "https://github.com/Netzvamp/cartoonista"
    },
    packages=["cartoons"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment"
    ],
    extras_require={
        'scraping': [
            "requests",
            "beautifulsoup4",
        ]
    },
    python_requires='>=3.6',
)