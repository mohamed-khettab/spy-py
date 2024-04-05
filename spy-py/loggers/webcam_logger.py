from cv2 import VideoCapture, imwrite
from os.path import join
import sys
from time import sleep
from config import LOGS_DIRECTORY_PATH, WEBCAM_INTERVAL, PICTURES_PER_EMAIL
from utils.utils import get_timestamp, log, handle_counter


class WebcamLogger:
    def __init__(self):
        self.logs_directory_path = LOGS_DIRECTORY_PATH if LOGS_DIRECTORY_PATH else ""
        self.error_file_path = join(LOGS_DIRECTORY_PATH, "errors.txt") if LOGS_DIRECTORY_PATH else "errors.txt"
        self.counter = 0
        self.counter_max = PICTURES_PER_EMAIL
        self.interval = WEBCAM_INTERVAL
        self.running = True

    def log_picture(self):
        cam = VideoCapture(0)
        sleep(0.5)
        result, image = cam.read()
        cam.release()

        if result:
            imwrite(join(self.logs_directory_path, f"webcam/{get_timestamp()}.png"), image)

    def handle_counter(self):
        self.counter += 1
        if handle_counter(self.counter, self.counter_max):
            pass  # TODO: Email logic here

    def run(self):
        try:
            while self.running:
                self.log_picture()
                self.handle_counter()
                sleep(self.interval)
        except KeyboardInterrupt:
            self.running = False
        except Exception as e:
            self.running = False
            self.log_error("AN ERROR OCCURRED WHILE LOGGING WEBCAM:", e)

    def log_error(self, message: str, exception: Exception) -> None:
        log(message, self.error_file_path)
        log(str(exception), self.error_file_path)


def main():
    webcam_logger = WebcamLogger()
    try:
        webcam_logger.run()
    except Exception:
        print("An error occurred while logging webcam.")
        print(f"See full error here: {webcam_logger.error_file_path}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
