import os
import datetime
import traceback

from utils.webhook_utils import send_log_file, send_message
from config import LOG_DIRECTORY_PATH


def log_to_file(log_file: str, data: str, mode="a") -> None:
    with open(os.path.join(LOG_DIRECTORY_PATH, log_file), mode) as f:
        f.write(data + "\n")


def log_info(info: str) -> None:
    print(f"[INFO]: {info}")
    with open(os.path.join(LOG_DIRECTORY_PATH, "log.txt"), "a") as f:
        f.write(f"[INFO]: {info}\n")


def log_warning(warning):
    print(f"[WARNING]: {warning}")
    with open(os.path.join(LOG_DIRECTORY_PATH, "log.txt"), "a") as f:
        f.write(f"[WARNING]: {warning}\n")


import traceback


def log_error(error):
    error_type = type(error).__name__
    error_message = str(error)
    error_traceback = traceback.format_exc()

    print(f"[ERROR]: {error_type}: {error_message}")
    print(f"Traceback:\n{error_traceback}")
    with open(os.path.join(LOG_DIRECTORY_PATH, "log.txt"), "a") as f:
        f.write(f"[ERROR]: {error_type}: {error_message}\n")
        f.write(f"Traceback:\n{error_traceback}\n")

    send_log_file(
        "`An error has occurred, sending logs...`",
        os.path.join(LOG_DIRECTORY_PATH, "log.txt"),
    )


def send_logs():
    send_log_file("`Sending logs...`", os.path.join(LOG_DIRECTORY_PATH, "log.txt"))


def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
