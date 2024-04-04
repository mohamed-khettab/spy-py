from PIL.ImageGrab import grab
from os.path import join
from os import _exit
from datetime import datetime
from time import sleep

from config import LOGS_DIRECTORY_PATH, SCREENSHOT_INTERVAL
from utils.tools import get_timestamp, log


class ScreenLogger:
    def __init__(self):
        self.logs_directory_path = (
            "" if not LOGS_DIRECTORY_PATH else LOGS_DIRECTORY_PATH
        )
        self.interval = SCREENSHOT_INTERVAL
        self.counter = 0
        self.running = True

    def screenshot(self):
        screenshot = grab()
        screenshot.save(
            join(self.logs_directory_path, f"screenshot_{get_timestamp()}.png")
        )
        screenshot.close()

    def run(self):
        try:
            while self.running:
                self.screnshot()
                sleep(self.interval)
        except KeyboardInterrupt:
            self.running = False
        except Exception as e:
            self.running = False
            log(f"AN ERROR OCCURED WHILE LOGGING SCREEN:", "errors.txt")
            log(e, "errors.txt")
            return 1

        return 0


def main():
    screen_logger = ScreenLogger()
    try:
        screen_logger.run()
    except Exception:
        screen_logger.running = False
        print("An error occured while logging screen.")
        print(f"See error here: ")  # TODO: put the file path to where the error log is


if __name__ == "__main__":
    _exit(main())
