import datetime
import os


def get_users(dir_path):
    """
    List files in directory.
    Ignore hidden files.
    Remove .txt extension from file name.
    Create dict with file name as key last modify datetime as value.
    """
    users = {}
    for file in os.listdir(dir_path):
        if file.startswith('.'):
            continue
        file_path = os.path.join(dir_path, file)
        if os.path.isfile(file_path):
            users[file.replace(".txt", "")] = convert_timestamp_to_datetime(os.path.getmtime(file_path))
    return users


def convert_timestamp_to_datetime(timestamp):
    """Convert timestamp to datetime string."""
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
