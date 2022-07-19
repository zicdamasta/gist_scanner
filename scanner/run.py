import os

from api.github import GetGithubGists
from api.pipedrive import PostPipedriveActivity
from datetime import datetime

import logging

logger = logging.getLogger(__name__)
logging_level = logging.getLevelName(os.environ.get('SCANNER_LOG_LEVEL', "INFO"))
logging.basicConfig(level=logging_level,
                    format='%(asctime)s %(levelname)-8s %(filename)s %(message)s',
                    datefmt='%d.%m.%Y '
                            '%H:%M:%S',
                    filename="logs/scanner.log",
                    filemode='a'
                    )


def parse_datetime(time: str) -> (str, str):
    """Convert ISO 8601 time (%Y-%m-%dT%H:%M:%SZ) to (%Y-%m-%d, %H:%M:%S) tuple."""
    dt = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
    return dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M:%S")


def get_activity_body(gist: dict) -> dict:
    """Get activity body."""
    created_at = gist["created_at"]
    due_date, due_time = parse_datetime(created_at)
    subject = next(iter(gist["files"]))
    public_description = generate_description(gist)
    return {
        "due_date": due_date,
        "due_time": due_time,
        "subject": subject,
        "public_description": public_description,
    }


def generate_description(gist: dict) -> str:
    url = gist["html_url"]
    user = gist["owner"]["login"]
    return f"Description: {gist['description']}<br>" \
           f"Owner: {user}" \
           f"<br>Link: <a href='{url}'>{url}</a>"


def convert_gist_to_pipedrive_activity(gist: dict):
    """Convert gist to pipedrive activity."""
    body = get_activity_body(gist)
    logger.info(f"Converting gist {gist['id']} to pipedrive activity")
    activity = PostPipedriveActivity(**body)
    if activity.get_status_code() != 201:
        logger.error(
            f"Error while posting activity to pipedrive with status code {activity.get_status_code()}. Body: {activity.get_json()}")
        return
    logger.info(f"Activity {gist['id']} added to pipedrive")


def parse_gists(username: str, since=""):
    """Parse gist."""
    logger.info(f"Scanning user {username}")
    gists = GetGithubGists(username, since)

    if gists.get_status_code() != 200:
        logger.error(
            f"Error while fetching gists for user {username} with status code {gists.get_status_code()}. Body: {gists.get_json()}")
        return

    gists = gists.get_json()
    logger.info(f"Found {len(gists)} gists for user {username}")
    logger.info(f"START CONVERTING GISTS TO PIPEDRIVE ACTIVITIES")
    for gist in gists:
        convert_gist_to_pipedrive_activity(gist)


def scan_users(users: list):
    """Scan users."""
    logger.info(f"Found {len(users)} user(s) in user list.")

    # if no users log error and raise error
    if not users:
        logger.error("No users to scan")
        raise Exception("No users to scan")
    logger.info(f"START SCANNING USERS")
    for user in users:
        parse_gists(user)


if __name__ == '__main__':
    users = ["ozubovasd", "ozubov"]
    scan_users(users)
