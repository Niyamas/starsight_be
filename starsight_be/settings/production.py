from .base import *

DEBUG = config('DEBUG', default=False, cast=bool)

try:
    from .local import *
except ImportError:
    pass
