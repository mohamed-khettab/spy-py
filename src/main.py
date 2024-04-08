import time
from core.loggers.browser_logger import BrowserLogger
from core.loggers.clipboard_logger import ClipboardLogger
from core.loggers.input_logger import InputLogger

browser_logger = BrowserLogger()
clipboard_logger = ClipboardLogger()
input_logger = InputLogger()
browser_logger.start()
clipboard_logger.start()
input_logger.start()
time.sleep(1)
browser_logger.stop()
clipboard_logger.stop()
input_logger.stop()