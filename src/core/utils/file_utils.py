from os import makedirs, listdir, remove
from os.path import exists, join, isfile, isdir

def create_log_directories(logs_directory_path: str) -> None:
    if not exists(logs_directory_path):
        makedirs(logs_directory_path)

    subdirectories = ["microphone", "webcam", "screenshots"]
    for subdirectory in subdirectories:
        subdirectory_path = join(logs_directory_path, subdirectory)
        if not exists(subdirectory_path):
            makedirs(subdirectory_path)


def clear_log_file(log_file_path: str) -> None:
    with open(log_file_path, "w"):
        pass


def clear_log_folder(log_directory_path: str) -> None:
    if exists(log_directory_path) and isdir(log_directory_path):
        for file_name in listdir(log_directory_path):
            file_path = join(log_directory_path, file_name)
            if isfile(file_path):
                remove(file_path)


def clear_logs(logs_directory_path: str) -> None:
    if exists(logs_directory_path) and isdir(logs_directory_path):
        for item_name in listdir(logs_directory_path):
            item_path = join(logs_directory_path, item_name)
            if isfile(item_path):
                remove(item_path)
            elif isdir(item_path):
                clear_log_folder(item_path)
