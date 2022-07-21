import logging
from datetime import datetime

from api.pipedrive import PostPipedriveActivity

logger = logging.getLogger(__name__)


def create_activity(gist: dict):
    """
    Convert Github gist to Pipedrive activity.

    :param gist: Github gist object with all the data needed to create a Pipedrive activity.
    """
    logger.info(f"Converting gist {gist['id']} to pipedrive activity")

    body = get_activity_body(gist)
    activity = PostPipedriveActivity(**body)

    if activity.get_status_code() != 201:
        message = f"Error while posting activity to Pipedrive with status code {activity.get_status_code()}. Body: {activity.get_json()}"
        logger.error(message)
        return

    logger.info(f"Activity {gist['id']} added to Pipedrive")


def get_activity_body(gist: dict) -> dict:
    """Extract needed params from gist and generate activity body."""
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
    """Generate description for activity."""
    url = gist["html_url"]
    user = gist["owner"]["login"]
    return f"Description: {gist['description']}<br>" \
           f"Owner: {user}" \
           f"<br>Link: <a href='{url}'>{url}</a>"


def parse_datetime(time: str) -> (str, str):
    """Convert ISO 8601 time (%Y-%m-%dT%H:%M:%SZ) to (%Y-%m-%d, %H:%M:%S) tuple."""
    dt = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
    return dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M:%S")
