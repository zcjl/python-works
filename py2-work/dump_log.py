import requests
import json
import time
import logging
import logging.handlers
 
LOG_FILE = 'test.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)
handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s')) 
logger = logging.getLogger(__name__).addHandler(handler).setLevel(logging.DEBUG)

def dump_log():
    while True:
        try:
            resp = requests.get('http://192.168.70.200:8102/', timeout=2).json()
            logger.info(resp)
            time.sleep(5)
        except Exception as e:
            tmp_traceback = traceback.format_exc()
            logger.error('[get_weight] failed. Please Check if weight_ip worked.')
            logger.error('[get_weight] exception: %s' % e)
            logger.error('[get_weight] traceback: %s' % tmp_traceback)
            break

dump_log()
