# -*- coding: utf-8 -*-
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("ease_grid")  # Use your actual package name
except PackageNotFoundError:
    __version__ = 'unknown'

from ease_grid.ease2_grid import *