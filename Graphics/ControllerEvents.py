import sys

import pygame

from pygame.locals import *

from multiprocessing import shared_memory

SPEED: int = 7
SHOUT_BUTTON: int = 10 # R1
pygame.init()
pygame.joystick.init()

class ControllerEvents:
    def __init__(self):
        global joystick
        self.clock = pygame.time.Clock()

        self.motion = [0, 0]

        if pygame.joystick.get_count() > 0:
            joystick = pygame.joystick.Joystick(0)

        else:
            raise Exception("Controller is not connected. Please connect controller")
    
        self.create_shm()

    def handle_events(self):
        """
        Handels all of the pygame events. Button press and joystick move
        """
        while True:
            events = pygame.event.get()
            for event in events:
                # Check if any button was pressed
                if event.type == JOYBUTTONDOWN:
                    # Check if R1 was pressed, to shot
                    if event.button == SHOUT_BUTTON:
                        self.shot()

                elif event.type == JOYBUTTONUP:
                    if event.button == SHOUT_BUTTON:
                        self.shared_list[2] = 0

                # Check if eny joystick moved
                if event.type == JOYAXISMOTION:
                    # Check if left joystick moved
                    if event.axis < 2: # Only left joystick [left h, left v, right h, right v]
                        self.motion[event.axis] = event.value if abs(event.value) >= 0.1 else 0

                # To exit window
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # Calc num steps horizntal
            steps_horizntal = round(self.motion[0] * SPEED)

            # Calc num steps vertical
            steps_vertical = round(self.motion[1] * SPEED)

            self.move(steps_horizntal, steps_vertical)

            self.clock.tick(60)

    def shot(self):
        """
        When R1 was preesed send the client a order to shot
        """
        self.shared_list[2] = 1

    def move(self, steps_horizntal: int, steps_vertical: int):
        """
        When joystick moved send the client num of steps in each diraction

        Args:
            steps_horizntal (int): stpes on the horizontal axis. Negative left, positive right.
            steps_vertical (int): stpes on the vertical axis. Negative up, positive down.
        """
        # If they are both 0 it means there is no need to move
        # So no need to send new location to the client
        if steps_horizntal == 0 and steps_vertical == 0: 
            self.shared_list[0] = 0
            self.shared_list[1] = 0
        else:
            self.shared_list[0] = steps_horizntal
            self.shared_list[1] = steps_vertical
        
    def create_shm(self):
        """
        Creates a shared memory list
        """
        try:
            self.shared_list = shared_memory.ShareableList([0,0,0], name="controller_mem")
        except:
            print("Shared memory already exists, resuming...")
            
    def use_shm(self, name: str):
        """
        Uses an existing shared memory list and reads from it
        """
        self.shared_list = shared_memory.ShareableList(name=name)
        return (self.shared_list[0], self.shared_list[1], self.shared_list[2])
        

gr = ControllerEvents()
gr.handle_events()