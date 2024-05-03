import requests
import os
from config import (
    LOG_DIRECTORY_PATH,
    DISCORD_WEBHOOK_URL,
    DISCORD_WEBHOOK_AVATAR_URL,
    DISCORD_WEBHOOK_USERNAME,
)


def send_message(message: str) -> int:
    data = {
        "content": message,
        "username": DISCORD_WEBHOOK_USERNAME,
        "avatar_url": DISCORD_WEBHOOK_AVATAR_URL,
    }
    response = requests.post(DISCORD_WEBHOOK_URL, data)
    return response.status_code


def send_log_files_in_directory(message: str, directory: str) -> int:
    files_dict = {}
    directory_path = os.path.join(LOG_DIRECTORY_PATH, directory)
    files = os.listdir(directory_path)

    for file_name in files:
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, "rb") as file:
                files_dict[file_name] = file.read()

    response = requests.post(
        DISCORD_WEBHOOK_URL,
        data={
            "content": message,
            "avatar_url": DISCORD_WEBHOOK_AVATAR_URL,
            "username": DISCORD_WEBHOOK_USERNAME,
        },
        files=files_dict,
    )
    return response.status_code


def send_log_file(message: str, file: str) -> int:
    file_path = os.path.join(LOG_DIRECTORY_PATH, file)
    with open(file_path, "rb") as file_data:
        files_dict = {os.path.basename(file_path): file_data.read()}

    response = requests.post(
        DISCORD_WEBHOOK_URL,
        data={
            "content": message,
            "avatar_url": DISCORD_WEBHOOK_AVATAR_URL,
            "username": DISCORD_WEBHOOK_USERNAME,
        },
        files=files_dict,
    )
    return response.status_code
