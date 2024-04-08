from core.spy import Spy
import sys

def main():
    spy = Spy()
    try:
        spy.start()
    except KeyboardInterrupt:
        spy.stop()
        print("Stopped successfully.")
    except Exception as e:
        print("An error occured: ", e)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())