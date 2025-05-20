import pigpio
import threading
from pigpio_dht import DHT11
import time

#source : https://github.com/garyns/pigpio-dht
class TempSensor(threading.Thread):
    def __init__(self, group = None, target = None, name = None, args = ..., kwargs = None, *, daemon = None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.kill = False
        self.result = {'temp_c': -1, 'temp_f': -1.0, 'humidity': -1, 'valid': True}
        gpio = 4 # BCM Numbering
        self.sensor = DHT11(gpio)
    def run(self):
        #Matrix Animation
        while not self.kill:
            try:
                temp_result = self.sensor.read()
                print(temp_result)
                if temp_result["valid"]:
                    self.result = temp_result
            except TimeoutError:
                print("sensor timout")
            except KeyboardInterrupt:
                self.kill = True
            except Exception:
                print("error unknown")