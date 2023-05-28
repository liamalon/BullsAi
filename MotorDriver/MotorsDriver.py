from multiprocessing import Process
import time
import board
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

SLEEP_TIME: float = 0.0006
PROCESS_TIMEOUT: int = 1

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
        self.released = False
        self.in_use = False

    def __del__(self):
        """
        Releases the motors when not in use
        """
        if not self.released:
            self.horizontal_motor.release()
            self.vertical_motor.release()
            self.released = True
        print("Released motors...")

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
            # In order to help it as a result of an heavy whieght 
            time.sleep(SLEEP_TIME * 5)


    def move_vertical(self, num_steps:int, backwards=False) -> None:
        """
        Moves the vertical motor (motor number 2)
        args:
            num_steps (int): number of steps to do
            backwards (bool): set to False by default but if true would move the other way
        returns:
            None
        """
        for step in range(num_steps):
            self.vertical_motor.onestep(direction=self.directions[backwards])
            time.sleep(SLEEP_TIME)

    
    def move_motors(self, steps_tuple: tuple=(0, 0)) -> None:
        """
        Moves both motors 
        args:
            steps_tuple (tuple): a tuple that contains num of steps in each axis (x_steps, y_steps) 
            [if x/y steps negetive would move in the other way]
        returns:
            None
        """                
        self.in_use = True
        
        x_steps = steps_tuple[0]
        y_steps = steps_tuple[1]
        
        horizontal_thread = Process(target=self.move_horizontal, args=(abs(x_steps), x_steps < 0))
        vertical_thread = Process(target=self.move_vertical, args=(abs(y_steps), y_steps < 0))

        # Starting new processes for each motor
        horizontal_thread.start()
        vertical_thread.start()

        # Waiting for them to end
        horizontal_thread.join(timeout=PROCESS_TIMEOUT)
        vertical_thread.join(timeout=PROCESS_TIMEOUT)

        self.in_use = False

