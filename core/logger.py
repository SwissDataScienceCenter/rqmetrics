"""Logger configuration."""
import logging
import sys

from core.config import LOG_LEVEL, LOG_FORMAT

logger = logging.getLogger('rqexporter')
logger.setLevel(LOG_LEVEL)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(LOG_FORMAT)
handler.setFormatter(formatter)
logger.addHandler(handler)
