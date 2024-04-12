from datetime import datetime
import os

from config.config import LOGS_DIRECTORY


def log_data(file_name, data, mode="a"):
    with open(os.path.join(LOGS_DIRECTORY, file_name), mode) as f:
        f.write(f"{timestamp()}: {data}\n")


def log_error(error):
    with open(os.path.join(LOGS_DIRECTORY, "errors.txt"), "a") as f:
        f.write(f"{timestamp()}: {error}\n")


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S")
