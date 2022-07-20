import logging

from scanner.api.github import GetGithubGists

from scanner.file_io import append_to_file, clear_file
from scanner.generate_activities import convert_gist_to_pipedrive_activity, get_activity_body

logger = logging.getLogger(__name__)


def parse_gists(username: str, since=""):
    """Parse gist."""
    logger.info(f"START SCANNING USER {username}")

    file_path = f"../server/api/gists/{username}.txt"
    clear_file(file_path)

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
