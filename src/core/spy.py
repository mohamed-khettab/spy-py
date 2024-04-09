from core.webhook import send_error

class Spy:
    def __init__(self) -> None:
        pass

    def start(self):
        pass
    

    def stop(self):
        pass

    def handle_error(self, e: Exception) -> int:
        send_error()
        pass # TODO: error handling logic