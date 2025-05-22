import pigpio
import threading
import time
class Timer(threading.Thread): # turns it's state to timeout when the designated time is reached.
    def __init__(self, group = None, target = None, name = None, args = ..., kwargs = None, *, daemon = None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.state = "running"
        self.last_time = time.time()
        self.kill = False
        self.timeout_value = 30
    def run(self):
        while not self.kill:
            if time.time() - self.last_time > self.timeout_value:
                self.state = "timeout" 
    def update_time(self):
        self.state = "running"
        self.last_time = time.time()
    def get_state(self):
        return self.state