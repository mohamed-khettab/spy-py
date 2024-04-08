from os.path import join
from time import sleep
from browserhistory import get_browserhistory
from config.config_loader import get_section_config


class BrowserLogger:
    def __init__(self):
        self.config = get_section_config("BROWSER")
        self.log_file_path = join(self.config["logs_directory_path"], "browser.txt")
        self.log_file_path = join(self.config["logs_directory_path"], "error.txt")
        self.counter = 0
        self.counter_max = int(self.config["logs_per_email"])
        self.interval = int(self.config["interval"])
        self.running = True
