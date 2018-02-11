import logging

writer = logging.getLogger('logger')
writer.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('msgs')
fh.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(message)s')
fh.setFormatter(formatter)
# add the handlers to the logger
writer.addHandler(fh)
