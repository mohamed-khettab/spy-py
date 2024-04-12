import cv2
import time
import os

from config.config import LOGS_DIRECTORY, WEBCAM_CAPTURE_INTERVAL, PICTURES_PER_EMAIL
from core.utils.logging_utils import log_error, timestamp


class WebcamLogger:
    def __init__(self):
        self.logs_directory = os.path.join(LOGS_DIRECTORY, "webcam")
        self.interval = WEBCAM_CAPTURE_INTERVAL
        self.running = False

    def log_picture(self):
        cam = cv2.VideoCapture(0)
        time.sleep(0.5)
        result, image = cam.read()
        cam.release()

        if result:
            cv2.imwrite(
                filename=os.path.join(self.logs_directory, f"{timestamp()}.png"),
                img=image,
            )
            print(os.path.join(self.logs_directory, f"{timestamp()}.png"))

    def run(self):
        try:
            self.log_picture()
            time.sleep(self.interval)
        except Exception as e:
            self.running = False
            log_error(e)
