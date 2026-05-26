
class LED:
    
    def turn_on(self):
        print("LED ON")
    
    def turn_off(self):
        print("LED OFF")
        
led1 = LED()
led2 = LED()
led3 = LED()

led = LED()
led.turn_on()
led.turn_off()

class Sensor:
    def __init__(self):
        self.name = "Temperature"
        self.value = 0
        
sensor = Sensor()

print(sensor.name)

sensor.value = 25

