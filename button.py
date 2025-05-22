import pigpio
import time
class Button:
    def __init__(self, pin,pi) -> None:
        self.pi = pi
        self.pin = pin
        self.isPressed = False
        self.count = 0
        self.is_button_just_released = False
        self.press_time = time.time()
        self.released_time = time.time()
        pi.set_mode(pin,pigpio.INPUT)
        pi.set_pull_up_down(pin,pigpio.PUD_UP)
        
    def detectPress(self):
        if self.pi.read(self.pin) == 0:
            if not self.isPressed:
                self.count += 1
                if self.count >= 4: # waits for for consecutive 0 reads
                    self.is_button_just_released = False
                    self.isPressed = True
                    self.press_time = time.time()
        else: # == 1
            if self.isPressed:
                self.released_time = time.time()
                self.is_button_just_released = True
            self.count = 0
            self.isPressed = False
    def getState(self):
        return self.isPressed
    def isReleased(self) -> float: # eats up the release and return the time if button just released
        if self.is_button_just_released:
            self.is_button_just_released = False
            return self.released_time - self.press_time
        return -1.0
