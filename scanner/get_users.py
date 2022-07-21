import logging
import os

logger = logging.getLogger(__name__)


def get_users() -> list:
    """
    Get users.
    USER_LIST_TYPE is 'env' - get users from env.
    USER_LIST_TYPE is 'file' - get users from file.
    """
    list_type = os.environ.get('USER_LIST_TYPE', 'env')
    match list_type:
        case 'file':
            filename = os.environ.get('USER_LIST_FILENAME', 'users.txt')
            return get_users_from_file(f"input/{filename}")
        case 'env':
            return get_users_from_env()
        case _:
            message = f"USER_LIST_TYPE is '{list_type}' but it should be 'file' or 'env'."
            logger.critical(message)
            raise Exception(message)


def get_users_from_env() -> list:
    """Get users from env."""
    logger.info("Getting users from USER_LIST env variable.")
    users = os.environ.get('USER_LIST')
    if not users:
        message = "USER_LIST_TYPE is 'env' but USER_LIST env variable is not set or empty."
        logger.critical(message)
        raise Exception(message)
    if not isinstance(users, list):
        users = convert_string_to_list(users)
    return users


def convert_string_to_list(string: str) -> list:
    """Convert string to list."""
    return string.strip().replace(" ", "").split(',')


def get_users_from_file(file_name: str) -> list:
    """Get users from file."""
    logger.info(f"Getting users from file. USER_LIST_FILENAME: {file_name}")
    try:
        with open(file_name, "r") as f:
            users = f.readlines()
    except FileNotFoundError:
        message = f"File {file_name} not found."
        logger.critical(message)
        raise Exception(message)

    return [user.strip() for user in users]
