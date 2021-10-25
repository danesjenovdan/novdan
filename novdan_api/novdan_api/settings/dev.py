import os

from .base import *

# Add general dev env settings here, but keep your local overrides in local.py

DEBUG = True

#

try:
    from .local import *
except ImportError:
    pass
