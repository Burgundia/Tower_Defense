import threading
import time


class Timer:
    def __init__(self, func, interval=1):
        self.func = func
        self.interval = interval
        self.active = False
        self.thread = None
        self.first_time = None

    def start(self):
        self.thread = threading.Thread(target=self.loop)
        self.active = True
        self.first_time = True
        self.thread.start()

    def loop(self):
        while self.active:
            if self.first_time:
                self.func()
                self.first_time = False
            time.sleep(self.interval)
            self.func()

    def stop(self):
        self.active = False
