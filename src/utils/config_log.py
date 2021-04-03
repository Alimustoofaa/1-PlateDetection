import os
import pytz
import logging
from pathlib import Path
from datetime import datetime
import logging.handlers as handlers

IST = pytz.timezone('Asia/Jakarta')

def datetime_format():
    datetime_now    = datetime.now(IST)
    year            = str(datetime_now.year)
    month           = '0'+str(datetime_now.month) if len(str(datetime_now.month)) == 1 else str(datetime_now.month)
    return year, month

def path_log():
    year, month = datetime_format()
    path = f'logger/{year}/{month}'
    Path(path).mkdir(parents=True, exist_ok=True)
    log_name = f'{path}/logging.log'
    return log_name

def logger(msg):
    log = logging.getLogger('uvicorn.access')
    log.setLevel(logging.INFO)

    # logHandler = handlers.TimedRotatingFileHandler(path_log(), when='D')
    # logFormatter = logging.Formatter('%(asctime)s | %(levelname)s : %(message)s')
    # logHandler.suffix = "%H-%M-%S_%d-%m-%Y.log"
    # logHandler.setLevel(logging.INFO)
    # logHandler.setFormatter(logFormatter)
    # log.addHandler(logHandler)
    # log.info(msg)
    # log.removeHandler(logHandler)
    fh = logging.FileHandler(path_log())
    logFormatter = logging.Formatter('%(asctime)s | %(levelname)s : %(message)s')
    fh.setFormatter(logFormatter)
    log.addHandler(fh)
    log.info(msg)
