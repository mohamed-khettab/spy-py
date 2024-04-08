from pyperclip import paste
from time import sleep
from os.path import join
import sys
from config.config_loader import get_section_config


class ClipboardLogger:
    def __init__(self):
        self.config = get_section_config("CLIPBOARD")
        self.log_file_path = join(self.config["logs_directory_path"], "clipboard.txt")
        self.error_file_path = join(self.config["logs_directory_path"], "errors.txt")
        self.counter = 0
        self.counter_max = self.config["pastes_per_email"]
        self.interval = self.config["interval"]
        self.running = True
