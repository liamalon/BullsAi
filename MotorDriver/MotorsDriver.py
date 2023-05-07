import threading
import time
import board
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
SLEEP_TIME = 0.01

class MotorsDriver:
    def __init__(self) -> None:
        """ 
        Initialises the variable kit to be our I2C Connected Adafruit Motor HAT.
        And sets up the motors
        """
        self.kit = MotorKit(i2c=board.I2C())
        self.horizontal_motor = self.kit.stepper1
        self.vertical_motor = self.kit.stepper2
        self.directions = [stepper.FORWARD, stepper.BACKWARD]

    def __del__(self):
        """
        Releases the motors when not in use
        """
        self.horizontal_motor.release()
        self.vertical_motor.release()

    def move_horizontal(self, num_steps:int, backwards=False) -> None:
        """
        Moves the horizontal motor (motor number 1)
        args:
            num_steps (int): number of steps to do
            backwards (bool): set to False by default but if true would move the other way
        returns:
            None
        """
        for step in range(num_steps):
            self.horizontal_motor.onestep(direction=self.directions[backwards])
            time.sleep(SLEEP_TIME)

    def move_vertical(self, num_steps:int, backwards=False) -> None:
        """
        Moves the vertical motor (motor number 1)
        args:
            num_steps (int): number of steps to do
            backwards (bool): set to False by default but if true would move the other way
        returns:
            None
        """
        for step in range(num_steps):
            self.vertical_motor.onestep(direction=self.directions[backwards])
            time.sleep(SLEEP_TIME)

    
    def move_motors(self, steps_tuple: tuple=(0,0)) -> None:
        """
        Moves both motors 
        args:
            steps_tuple (tuple): a tuple that contains num of steps in each axis (x_steps, y_steps) 
            [if x/y steps negetive would move in the other way]
        returns:
            None
        """
        x_steps = steps_tuple[0]
        y_steps = steps_tuple[0]

        self.move_horizontal(abs(x_steps), x_steps < 0)
        self.move_vertical(abs(y_steps), y_steps < 0)

