import logging
from .helpers import full_path

class HopLogFileHandler(logging.FileHandler):
    def __init__(self, filename):
        path = full_path('~/.hop/logs')

        super(HopLogFileHandler, self).__init__(path + '/' + filename)
