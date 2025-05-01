import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = RotatingFileHandler(
    'app.log', 
    maxBytes=1024*1024, 
    backupCount=5,
    encoding='utf-8'
)
formatter = logging.Formatter('%(asctime)s - Server - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)