import logging

from api.github import GetGithubGists

from file_io import append_to_file, clear_file
from generate_activities import generate_activities

logger = logging.getLogger(__name__)


def get_gists(username: str, file_path: str, since="", ):
    gists = GetGithubGists(username, since)

    if gists.get_status_code() != 200:
        message = f"Error while getting user for user {username} with status code {gists.get_status_code()}. Body: {gists.get_json()}"
        logger.error(message)
        append_to_file(message, file_path)
        return {}

    return gists.get_json()


def parse_gists(username: str, since=""):
    """
    Parse user gists and pass them to activity converter.

    :param username: username of the user
    :param since: added gists after the given time. Format: YYYY-MM-DDTHH:MM:SSZ.
    """
    logger.info(f"Start scanning user {username}")

    file_path = f"output/user/{username}.txt"
    clear_file(file_path)

    gists = get_gists(username, file_path, since)

    logger.info(f"Found {len(gists)} gists for user {username}")

    if not gists:
        append_to_file(f"No GitHub gists added since {since} UTC time.", file_path)
        return

    generate_activities(file_path, gists, since)
