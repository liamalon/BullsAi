from typing import Tuple
import numpy as np
class EnemyTargeting:
    """
    EnemyTargeting is a class that is in charge
    with everything that has to do with targeting an 
    enemy
    """
    def __init__(self, step_size:int):
        self.step_size = step_size

    def GetCenterOfPeople(self, people: Tuple):
        """
        Args:
            people (Tuple): a tuple containing
            (top left x, top left y, width, height, confidence)
        
        Returns:
            center (tuple): a tuple of (center x, center y)
        """

        # Finding the X of the center
        x = int(np.average([people[0], people[2]]))

        # Finding the Y of the center 
        y = int(np.average([people[1], people[3]]))

        # Return center tuple
        return (x, y)
    
    def CenterTarget(self, current_x:int, current_y:int, people: Tuple):
        """
        Args:
            current_x (int): the current x of the target
            current_y (int): the current y of the target
        
        Returns:
            steps (tuple): a tuple that contains num of steps for each diraction
            horizontal (int): if positive to the left if negetive to the right
            vertical (int): if positive up if negetive down
            (horizontal, vertical)
        """

        # New target location
        center = self.GetCenterOfPeople(people)

        # TODO: current_xy - center // num_steps





        