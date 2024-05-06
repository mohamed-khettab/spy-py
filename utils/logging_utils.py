import os
import datetime

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


def log_error(error):
    print(f"[ERROR]: {error}")
    global counter
    with open(os.path.join(LOG_DIRECTORY_PATH, "log.txt"), "a") as f:
        f.write(f"[ERROR]: {error}\n")
    counter = 0
    send_log_file(
        "`An error has occurred, sending logs...`",
        os.path.join(LOG_DIRECTORY_PATH, "log.txt"),
    )


def send_logs():
    send_log_file("`Sending logs...`", os.path.join(LOG_DIRECTORY_PATH, "log.txt"))

def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")