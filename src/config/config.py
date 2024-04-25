import os
import tempfile


# Common Configuration
LOGS_DIRECTORY = "/Users/mohamedkhettab/Desktop/Coding/Python/keylogger-v2/src"  # Path to wherever you want the logs directory to be
if not LOGS_DIRECTORY:
    LOGS_DIRECTORY = os.path.join(tempfile.gettempdir(), "logs")
else:
    LOGS_DIRECTORY = os.path.join(LOGS_DIRECTORY, "logs")

# Webhook Configuration
WEBHOOK_URL = "" # URL To your discord webhook
WEBHOOK_AVATAR_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Skull_and_Crossbones.svg/510px-Skull_and_Crossbones.svg.png?20190922182140" # URL to your webhook's avatar
WEBHOOK_USERNAME = "spy-py" # What you want the webhook username to be

# Input Configuration
LOGS_PER_EMAIL = 10000  # Number of logged events before sending the data

# Microphone Configuration
MICROPHONE_RECORDING_INTERVAL = 60  # Length of each microphone recording (in seconds)
MICROPHONE_RECORDINGS_PER_EMAIL = 300  # Number of recordings before sending the data

# Screen Configuration
SCREENSHOT_INTERVAL = 60  # Time interval for taking screenshots (in seconds)
SCREENSHOTS_PER_EMAIL = 300  # Number of screenshots before sending the data

# Webcam Configuration
WEBCAM_CAPTURE_INTERVAL = 60  # Time interval for capturing webcam pictures (in seconds)
PICTURES_PER_EMAIL = 300  # Number of pictures before sending the data

# Clipboard Configuration
CLIPBOARD_LOG_INTERVAL = 500  # Time interval for logging clipboard events (in seconds)
PASTES_PER_EMAIL = 20  # Number of clipboard events before sending the data

# Browser Configuration
BROWSER_LOG_INTERVAL = 20000  # Time interval for logging browser events (in seconds)
BROWSER_LOGS_PER_EMAIL = 1  # Number of browser logs before sending the data
