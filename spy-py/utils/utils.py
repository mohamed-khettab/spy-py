from datetime import datetime
from os.path import exists, join
from os import makedirs


def log(data: str, log_file_path: str, timestamp: bool = True) -> None:
    with open(log_file_path, "a") as f:
        if timestamp:
            f.write(f"{get_timestamp()}: {data}\n")
        else:
            f.write(f"{data}\n")


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def handle_counter(count, counter_max):
    if count >= counter_max:
        return True
    else:
        return False


def create_log_directories(logs_directory_path):
    if not exists(logs_directory_path):
        makedirs(logs_directory_path)

    subdirectories = ["microphone", "webcam", "screenshots"]
    for subdirectory in subdirectories:
        subdirectory_path = join(logs_directory_path, subdirectory)
        if not exists(subdirectory_path):
            makedirs(subdirectory_path)


# TODO: clear log file
def clear_log_file(log_file_path):
    pass


# TODO: Clear log folders
def clear_log_folder(log_directory_path):
    pass


# TODO: clear all logs
def clear_logs(logs_directory_path):
    pass
