from cv2 import VideoCapture, imwrite, waitKey
from os.path import join
from os import _exit
from time import sleep

from config import LOGS_DIRECTORY_PATH, WEBCAM_INTERVAL, PICTURES_PER_EMAIL
from utils.tools import get_timestamp, log, handle_counter


class WebcamLogger:
    def __init__(self):
        self.interval = WEBCAM_INTERVAL
        self.logs_directory_path = (
            "" if not LOGS_DIRECTORY_PATH else LOGS_DIRECTORY_PATH
        )
        self.counter = 0
        self.counter_max = PICTURES_PER_EMAIL
        self.running = True

    def take_picture(self):
        cam = VideoCapture(0)
        result, image = cam.read()

        if result:
            imwrite(join(LOGS_DIRECTORY_PATH, f"{get_timestamp()}.png"), image)

    def run(self):
        try:
            while self.running:
                self.take_picture()
                sleep(self.interval)
                self.counter += 1
                if handle_counter(self.counter, self.counter_max):
                    pass # TODO: email logic
        except KeyboardInterrupt:
            self.running = False
        except Exception as e:
            self.running = False
            log("AN ERROR OCCURED WHILE LOGGING WEBCAM:", "errors.txt")
            log(e, "errors.txt")
            return 1

        return 0


def main():
    webcam_logger = WebcamLogger()
    try:
        WebcamLogger.run()
    except Exception:
        webcam_logger.running = False
        print("An error occured while logging webcam.")
        print(
            "See full error here: "
        )  # TODO: Show the file path of where the error log is

if __name__ == "__main__":
    _exit(main())