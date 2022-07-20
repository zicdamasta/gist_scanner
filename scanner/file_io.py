import logging

logger = logging.getLogger(__name__)


def append_to_file(content: str, file_name: str):
    """Write users to file."""
    logger.info(f"Appending to file {file_name}. Content: {content}")
    with open(file_name, "a") as f:
        f.write(content + "\n")


def clear_file(file_name: str):
    logger.info(f"Clearing file {file_name}")
    with open(file_name, "w") as f:
        f.write("")
