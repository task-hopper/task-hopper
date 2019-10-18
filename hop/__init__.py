import json
import logging
import logging.config
import pkg_resources
from os.path import exists

from .helpers import full_path
from .hop_log_file_handler import HopLogFileHandler

# verify required directories

#  TODO rethink/remove validation
required_directories = ['~/.hop', '~/.hop/logs']
is_missing_directories = any((not exists(full_path(p))) for p in required_directories)
if is_missing_directories:
    print('missing required directores ~/.hop and ~/.hop/logs')

# create logger
log_config = pkg_resources.resource_filename(__name__, 'ext/logger_config.json')
with open(log_config, 'r') as config_file:
    config_dict = json.load(config_file)

logging.handlers.HopLogFileHandler = HopLogFileHandler
logging.config.dictConfig(config_dict)
logger = logging.getLogger(__name__)
logger.info('Completed logging configuration')
