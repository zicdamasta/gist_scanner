import os

import logging

from scanner.scan_users import scan_users

logger = logging.getLogger(__name__)
logging_level = logging.getLevelName(os.environ.get('SCANNER_LOG_LEVEL', "DEBUG"))
logging.basicConfig(level=logging_level,
                    format='%(asctime)s %(levelname)-8s %(filename)s %(message)s',
                    datefmt='%d.%m.%Y '
                            '%H:%M:%S',
                    handlers=[
                        logging.FileHandler("logs/scanner.log"),
                        logging.StreamHandler()
                    ]
                    )

if __name__ == '__main__':
    h_interval = os.environ.get('SCANNER_HOUR_INTERVAL', 3)
    m_interval = os.environ.get('SCANNER_MINUTE_INTERVAL', 0)

    users = ["ozubovasd", "ozubov", "Jose26398", "ngocanhnckh", "abuxton"]
    scan_users(users, h_interval, m_interval)
