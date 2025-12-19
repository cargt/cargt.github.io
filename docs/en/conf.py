# Configuration file for the Sphinx documentation builder.

import os
import sys

# Add parent directory to path to import conf_common
sys.path.insert(0, os.path.abspath('..'))

# Import common configuration
from conf_common import *

# Language-specific configuration
language = 'en'

# The version info for the project
version = '1.0'
release = '1.0.0'
