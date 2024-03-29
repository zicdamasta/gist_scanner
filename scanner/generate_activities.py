import logging

from create_activity import get_activity_body, create_activity
from file_io import append_to_file

logger = logging.getLogger(__name__)


def generate_activities(file_path, gists, since):
    """
    Generate activities from gists.

    :param file_path: file path to write results to
    :param gists: gists to generate activities from
    :param since: timestamp used in github api to fetch gists added after that datetime
    """
    logger.info("Start converting gists to Pipedrive activities.")
    append_to_file(f"{len(gists)} gists added since {since} UTC time.", file_path)
    for gist in gists:
        append_to_file(str(get_activity_body(gist)), file_path)
        create_activity(gist)
