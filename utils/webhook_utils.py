import requests
import os
import time
from config import LOG_DIRECTORY_PATH, DISCORD_WEBHOOK_URL, DISCORD_WEBHOOK_AVATAR_URL, DISCORD_WEBHOOK_USERNAME


def send_message(message):
    data = {
        "content": message,
        "username": DISCORD_WEBHOOK_USERNAME,
        "avatar_url": DISCORD_WEBHOOK_AVATAR_URL,
    }
    response = requests.post(DISCORD_WEBHOOK_URL, data)
    return response.status


def send_log_files_in_directory(message, directory):
    files_dict = {
        "content": message,
        "avatar_url": DISCORD_WEBHOOK_AVATAR_URL,
        "username": DISCORD_WEBHOOK_USERNAME,
    }
    directory_path = os.path.join(LOG_DIRECTORY_PATH, directory)
    files = os.listdir(directory_path)

    for file_name in files:
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, "rb") as file:
                files_dict[file_name] = file.read()

    response = requests.post(DISCORD_WEBHOOK_URL, files=files_dict)
    return response.status_code


def send_log_file(message, file):
    files_dict = {
        "content": message,
        "avatar_url": DISCORD_WEBHOOK_AVATAR_URL,
        "username": DISCORD_WEBHOOK_USERNAME,
    }
    files_dict[os.path.basename(os.path.join(LOG_DIRECTORY_PATH, file))] = open(os.path.join(LOG_DIRECTORY_PATH, file), "rb").read()
    response = requests.post(DISCORD_WEBHOOK_URL, files=files_dict)
    return response.status_code
