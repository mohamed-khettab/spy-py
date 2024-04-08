from core.spy import Spy
from time import sleep

def main():
    spy = Spy()
    spy.start()
    sleep(5)
    print("stopping...")
    spy.stop()

if __name__ == "__main__":
    main()