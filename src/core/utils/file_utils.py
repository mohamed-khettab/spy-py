import os


def create_log_directories(logs_directory_path: str) -> None:
    if not os.path.exists(logs_directory_path):
        os.makedirs(logs_directory_path)

    subdirectories = ["microphone", "webcam", "screenshots"]
    for subdirectory in subdirectories:
        subdirectory_path = os.path.join(logs_directory_path, subdirectory)
        if not os.path.exists(subdirectory_path):
            os.makedirs(subdirectory_path)


def clear_log_file(log_file_path: str) -> None:
    with open(log_file_path, "w"):
        pass


def clear_log_folder(log_directory_path: str) -> None:
    if os.path.exists(log_directory_path) and os.path.isdir(log_directory_path):
        for file_name in os.listdir(log_directory_path):
            file_path = os.path.join(log_directory_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)


def clear_logs(logs_directory_path: str) -> None:
    if os.path.exists(logs_directory_path) and os.path.isdir(logs_directory_path):
        for item_name in os.listdir(logs_directory_path):
            item_path = os.path.join(logs_directory_path, item_name)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                clear_log_folder(item_path)
