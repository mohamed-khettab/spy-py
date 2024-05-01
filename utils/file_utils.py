import os
from config import LOG_DIRECTORY_PATH

def create_log_directories() -> None:
    if not os.path.exists(LOG_DIRECTORY_PATH):
        os.makedirs(LOG_DIRECTORY_PATH)

    subdirectories = ["microphone", "webcam", "screenshots"]
    for subdirectory in subdirectories:
        subdirectory_path = os.path.join(LOG_DIRECTORY_PATH, subdirectory)
        if not os.path.exists(subdirectory_path):
            os.makedirs(subdirectory_path)


def clear_files_in_log_directory(directory: str) -> None:
    directory_path = os.path.join(LOG_DIRECTORY_PATH, directory)
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        for item_name in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item_name)
            if os.path.isfile(item_path):
                os.remove(item_path)

def clear_log_file(file: str) -> None:
    file_path = os.path.join(LOG_DIRECTORY_PATH, file)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        os.remove(file_path)