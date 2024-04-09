import os
import tempfile

# Common Configuration
LOGS_DIRECTORY = "/Users/mohamedkhettab/Desktop/Coding/Python/keylogger-v2/src"

if not LOGS_DIRECTORY:
    LOGS_DIRECTORY = os.path.join(tempfile.gettempdir(), "logs")

# Input Configuration
LOGS_PER_EMAIL = 10000  # Number of logged events before sending an email

# Microphone Configuration
MICROPHONE_RECORDING_INTERVAL = 60  # Length of each microphone recording (in seconds)
MICROPHONE_RECORDINGS_PER_EMAIL = 300  # Number of recordings before sending an email

# Screen Configuration
SCREENSHOT_INTERVAL = 60  # Time interval for taking screenshots (in seconds)
SCREENSHOTS_PER_EMAIL = 300  # Number of screenshots before sending an email

# Webcam Configuration
WEBCAM_CAPTURE_INTERVAL = 60  # Time interval for capturing webcam pictures (in seconds)
PICTURES_PER_EMAIL = 300  # Number of pictures before sending an email

# Clipboard Configuration
CLIPBOARD_LOG_INTERVAL = 500  # Time interval for logging clipboard events (in seconds)
PASTES_PER_EMAIL = 20  # Number of clipboard events before sending an email

# Browser Configuration
BROWSER_LOG_INTERVAL = 20000  # Time interval for logging browser events (in seconds)
BROWSER_LOGS_PER_EMAIL = 1  # Number of browser logs before sending an email
