import os
import signal

from core.spy import Spy


def signal_handler(sig, frame):
    print("Exiting...")
    os._exit(0)


signal.signal(signal.SIGINT, signal_handler)


def main():
    spy = Spy()
    try:
        spy.start()
        signal.pause()
    except Exception as e:
        print("An error occurred: %s", e)
    finally:
        spy.handle_error()
        print("Spy stopped.")

    return 0


if __name__ == "__main__":
    main()
