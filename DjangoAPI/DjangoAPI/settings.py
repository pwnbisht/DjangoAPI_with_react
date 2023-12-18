import os
import ssl
from pathlib import Path

from decouple import config

if env('ENV') == 'prod':
    from .settings_prod import *
else:
    from .settings_dev import *

