# logging_config.py #

#import sys
#import os

# Add the path to the project's root directory
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from logging.handlers import RotatingFileHandler

def configure_logging(app):
    handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)


