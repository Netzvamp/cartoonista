"""
A cartoon library.

requirements: requests, beautifulsoup4
"""
from .cartoonist import Cartoonist as Cartoons
from .nichtlustig import nichtlustig
from .ruthe import ruthe
from .perscheid import perscheid
from .xkcd import xkcd
from .islieb import islieb
from .schoenescheisse import schoenescheisse
from .explosm import explosm
from .exceptions import CartoonError

__version__ = "0.4.1"
