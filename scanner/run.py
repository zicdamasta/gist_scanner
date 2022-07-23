import os

import logging

from scan_users import scan_users
from apscheduler.schedulers.blocking import BlockingScheduler

from get_users import get_users

logger = logging.getLogger(__name__)
logging_level = logging.getLevelName(os.environ.get('SCANNER_LOG_LEVEL', "DEBUG"))
logging.basicConfig(level=logging_level,
                    format='%(asctime)s %(levelname)-8s %(filename)s %(message)s',
                    datefmt='%d.%m.%Y '
                            '%H:%M:%S',
                    handlers=[
                        logging.FileHandler("./logs/scanner.log"),
                        logging.StreamHandler()
                    ]
                    )


def run():
    h_interval = int(os.environ.get('SCANNER_HOUR_INTERVAL', 3))
    m_interval = int(os.environ.get('SCANNER_MINUTE_INTERVAL', 0))
    users = get_users()

    scan_users(users, h_interval, m_interval)

    scheduler = BlockingScheduler()
    scheduler.add_job(scan_users, 'interval',
                      args=(users, h_interval, m_interval),
                      hours=h_interval,
                      minutes=m_interval)
    scheduler.start()


if __name__ == '__main__':
    run()
