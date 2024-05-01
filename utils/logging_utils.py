import os

from utils.webhook_utils import send_file, send_message
from config import LOGS_DIRECTORY, LOG_ENTRIES_BEFORE_SEND

counter = 0

def log_to_file(log_file, data):
    with open(os.path.join(LOGS_DIRECTORY, log_file), 'a') as f:
        f.write(data + '\n')

def log_info(info):
   print(f"[INFO]: {info}")
   with open(os.path.join(LOGS_DIRECTORY, 'log.txt'), 'a') as f:
       f.write(info + '\n')
   handle_counter()

def log_warning(warning):
    print(f"[WARNING]: {warning}")
    with open(os.path.join(LOGS_DIRECTORY, 'log.txt'), 'a') as f:
        f.write(warning + '\n')
    handle_counter()

def log_error(error):
    print(f"[ERROR]: {error}")
    send_message("An error has occurred, sending logs...")
    global counter
    with open(os.path.join(LOGS_DIRECTORY, 'log.txt'), 'a') as f:
        f.write(error + '\n')
    counter = 0
    send_file(os.path.join(LOGS_DIRECTORY, 'log.txt'))

def handle_counter():
    global counter
    counter += 1
    if counter > LOG_ENTRIES_BEFORE_SEND:
        send_file(os.path.join(LOGS_DIRECTORY, 'log.txt'))
        counter = 0