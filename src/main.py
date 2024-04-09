from core.spy import Spy
import os

def main():
    spy = Spy()
    try:
        spy.start()
    except KeyboardInterrupt:
        spy.stop()
    except Exception:
        spy.stop()
        spy.handle_error()
        return 1
    return 0

if __name__ == "__main__":
    os._exit(main())