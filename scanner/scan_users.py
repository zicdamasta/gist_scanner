import logging
from datetime import datetime, timedelta

from parse_gists import parse_gists

logger = logging.getLogger(__name__)


def calculate_since(hours_interval: int, minutes_interval: int):
    """Calculate since time."""
    since = datetime.utcnow() - timedelta(hours=hours_interval, minutes=minutes_interval)
    return since.strftime("%Y-%m-%dT%H:%M:%SZ")


def scan_users(users: list, hours_interval: int, minutes_interval: int):
    """
    Scan list of users and pass them to user parser.

    :param users: list of users
    :param hours_interval: scan interval in hours
    :param minutes_interval: scan interval in minutes
    """

    logger.info(f"Found {len(users)} user(s) in user list.")

    if not users:
        message = "No users found in user list"
        logger.exception(message)

    since = calculate_since(hours_interval, minutes_interval)
    logger.info("Start scanning users.")
    for user in users:
        parse_gists(user, since)
