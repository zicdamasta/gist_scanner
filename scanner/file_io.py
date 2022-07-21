import logging

logger = logging.getLogger(__name__)


def append_to_file(content: str, file_name: str):
    """Append content to file."""
    logger.info(f"Appending to file {file_name}. Content: {content}")
    try:
        with open(file_name, "a") as f:
            f.write(content + "\n")
    except FileNotFoundError:
        message = f"File {file_name} not found while trying to append."
        logger.exception(message)


def clear_file(file_name: str):
    """Clear file."""
    logger.info(f"Clearing file {file_name}")
    try:
        with open(file_name, "w") as f:
            f.write("")
    except FileNotFoundError:
        message = f"File {file_name} not found while trying to clear."
        logger.exception(message)
