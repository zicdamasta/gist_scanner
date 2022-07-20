import os

from api.github import GetGithubGists
from api.pipedrive import PostPipedriveActivity
from datetime import datetime, timedelta

import logging

logger = logging.getLogger(__name__)
logging_level = logging.getLevelName(os.environ.get('SCANNER_LOG_LEVEL', "DEBUG"))
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


def clear_file(file_name: str):
    """Clear file."""
    with open(file_name, "w") as f:
        pass


def append_to_file(content: str, file_name: str):
    """Write users to file."""
    with open(file_name, "a") as f:
        f.write(content + "\n")


def generate_description(gist: dict) -> str:
    url = gist["html_url"]
    user = gist["owner"]["login"]
    return f"Description: {gist['description']}<br>" \
           f"Owner: {user}" \
           f"<br>Link: <a href='{url}'>{url}</a>"


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


def convert_gist_to_pipedrive_activity(gist: dict):
    """Convert gist to pipedrive activity."""
    logger.info(f"Converting gist {gist['id']} to pipedrive activity")

    body = get_activity_body(gist)
    activity = PostPipedriveActivity(**body)

    if activity.get_status_code() != 201:
        logger.error(
            f"Error while posting activity to Pipedrive with status code {activity.get_status_code()}. Body: {activity.get_json()}")
        return

    logger.info(f"Activity {gist['id']} added to Pipedrive")


def parse_gists(username: str, since=""):
    """Parse gist."""
    file_path = f"../server/api/gists/{username}.txt"
    clear_file(file_path)

    logger.info(f"Scanning user {username}")

    gists = GetGithubGists(username, since)

    if gists.get_status_code() != 200:
        message = f"Error while getting gists for user {username} with status code {gists.get_status_code()}. Body: {gists.get_json()}"
        logger.error(message)
        append_to_file(message, file_path)
        return

    gists = gists.get_json()

    logger.info(f"Found {len(gists)} gists for user {username}")

    if not gists:
        append_to_file(f"No gists added since {since} UTC time.", file_path)
        return

    logger.info(f"START CONVERTING GISTS TO PIPEDRIVE ACTIVITIES")
    append_to_file(f"{len(gists)} gists added since {since} UTC time.", file_path)

    for gist in gists:
        append_to_file(str(get_activity_body(gist)), file_path)
        convert_gist_to_pipedrive_activity(gist)


def calculate_since(hours_interval: int, minutes_interval: int):
    """Calculate since."""
    since = datetime.utcnow() - timedelta(hours=hours_interval, minutes=minutes_interval)
    return since.strftime("%Y-%m-%dT%H:%M:%SZ")


def scan_users(users: list, hours_interval: int, minutes_interval: int):
    """Scan users."""
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


if __name__ == '__main__':
    h_interval = os.environ.get('SCANNER_HOUR_INTERVAL', 3)
    m_interval = os.environ.get('SCANNER_MINUTE_INTERVAL', 0)

    users = ["ozubovasd", "ozubov", "Jose26398", "ngocanhnckh", "abuxton"]
    scan_users(users, h_interval, m_interval)
