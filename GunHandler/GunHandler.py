import RPi.GPIO as GPIO
import time
RELAY_PIN = 21
SLEEP_TIME = 0.1

class Gun:
    def __init__(self) -> None:
        """
        Inits pin 21 in oreder fot it to be ready for use
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RELAY_PIN, GPIO.OUT)
        GPIO.output(RELAY_PIN, GPIO.LOW)
        self.fire = False
        self.runnig = True
    
    def fire_gun(self):
        """
        Makes the gun fire,
        in order to fire the gun we need to set pin 21 to high
        for the electrical circut to close and the gun get power
        """
        while self.runnig:
            if self.fire:
                GPIO.output(RELAY_PIN, GPIO.HIGH)
                time.sleep(SLEEP_TIME)
                GPIO.output(RELAY_PIN, GPIO.LOW)
                self.fire = False    

if __name__ == "__main__":
    gn = Gun()
    gn.fire()