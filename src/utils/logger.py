import os
import pytz
import logging
from pathlib import Path
from datetime import datetime

class Logger(object):
    def __init__(self):
        self.ist = pytz.timezone('Asia/Jakarta')
        self.log = logging.getLogger('uvicorn.access')
        self.datetime_format()
        self.logger()

    def datetime_format(self):
        datetime_now         = datetime.now(self.ist)
        self.year            = str(datetime_now.year)
        self.month           = '0'+str(datetime_now.month) if len(str(datetime_now.month)) == 1 else str(datetime_now.month)
        self.day             = '0'+str(datetime_now.day) if len(str(datetime_now.day)) == 1 else str(datetime_now.day)
        self.hour            = '0'+str(datetime_now.hour) if len(str(datetime_now.hour)) == 1 else str(datetime_now.hour)
        self.minute          = '0'+str(datetime_now.minute) if len(str(datetime_now.minute)) ==(str(datetime_now.minute)) == 1 else str(datetime_now.minute)
        # return year, month, day
    
    def formater_time_log(self, *args):
        return datetime.now(self.ist).timetuple()

    def path_log(self):
        path = f'logger/{self.year}/{self.month}'
        Path(path).mkdir(parents=True, exist_ok=True)
        return  f'{path}/logging'

    def logger(self):
        rfh = logging.handlers.TimedRotatingFileHandler(
            filename = self.path_log(),
            when='M'
        )
        rfh.suffix = "%H-%M-%S_%d-%m-%Y.log"
        logging.Formatter.converter = self.formater_time_log
        logging.basicConfig(handlers = [rfh],
                            level=logging.INFO, 
                            format=f'%(asctime)s | %(levelname)s : %(message)s')
