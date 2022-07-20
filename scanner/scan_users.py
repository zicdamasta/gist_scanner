import logging
from datetime import datetime, timedelta

from scanner.file_io import append_to_file, clear_file
from scanner.parse_gists import parse_gists

logger = logging.getLogger(__name__)


def scan_users(users: list, hours_interval: int, minutes_interval: int):
    """
    Scan list of users and pass them to gists parser.

    :param users: list of users
    :param hours_interval: scan interval in hours
    :param minutes_interval: scan interval in minutes
    """
    users_file = "../server/api/users.txt"
    clear_file(users_file)

    logger.info(f"Found {len(users)} user(s) in user list.")

    if not users:
        message = "No users found in user list"
        logger.error(message)
        append_to_file(message, "../server/api/users.txt")
        raise Exception(message)

    since = calculate_since(hours_interval, minutes_interval)
    logger.info(f"START SCANNING USERS")
    for user in users:
        append_to_file(user, users_file)
        parse_gists(user, since)


def calculate_since(hours_interval: int, minutes_interval: int):
    """Calculate since time."""
    since = datetime.utcnow() - timedelta(hours=hours_interval, minutes=minutes_interval)
    return since.strftime("%Y-%m-%dT%H:%M:%SZ")
