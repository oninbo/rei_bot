import logging
from logging.handlers import RotatingFileHandler

log_file = 'logs/logs.txt'

logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = RotatingFileHandler(log_file, maxBytes=10000)
fh.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(ch)
logger.addHandler(fh)

