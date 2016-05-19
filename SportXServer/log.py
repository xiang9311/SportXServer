__author__ = '祥祥'
import logging

# log
logger = logging.getLogger('django')

def info(content):
    print(content)
    logger.info(content)

def debug(content):
    print(content)
    logger.debug(content)

def warn(content):
    print(content)
    logger.warn(content)

def error(content):
    print(content)
    logger.error(content)