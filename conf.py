import logging
import os
import sys

LOG_LEVEL = os.environ.get('LOG_LEVEL')
PORT = os.environ.get('PORT')

if LOG_LEVEL is None:
    LOG_LEVEL = 'INFO'
if PORT is None:
    PORT = '3000'

logging.basicConfig(stream=sys.stdout,
                    level=os.environ.get('LOG_LEVEL'),
                    format='%(levelname)s %(asctime)s %(message)s')

Logger = logging.getLogger()
Logger.setLevel(LOG_LEVEL)
