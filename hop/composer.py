import atexit

from hop.core.composer import Composer

composer = Composer()
atexit.register(composer._flush)
