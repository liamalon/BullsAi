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

    def get_center_of_people(self, people: Tuple):
        """
        Gets the center of the people
        Args:
            people (Tuple): a tuple containing
            (top left x, top left y, buttom right x, buttom right y, confidence)
        
        Returns:
            center (tuple): a tuple of (center x, center y)
        """

        # Finding the X of the center
        x = np.average([people[0], people[2]]).astype(int)

        # Finding the Y of the center 
        y = np.average([people[1], people[3]]).astype(int)

        # Return center tuple
        return (x, y)
    
    def get_steps_to_people_center(self, current_x:int, current_y:int, people: Tuple):
        """
        Gets the steps to the people center
        Args:
            current_x (int): the current x of the target (usually the x of center of the frame at the moment)
            current_y (int): the current y of the target (usually the y of center of the frame at the moment)
            people (tuple(x, y, w, h, confidence)): all the boxes and locations
            of people in the frame 
        Returns:
            steps (tuple): a tuple that contains num of steps for each diraction
            horizontal (int): if positive to the left if negetive to the right
            vertical (int): if positive down if negetive up
            (horizontal, vertical)
        """

        # New target location
        new_center_x, new_center_y = self.GetCenterOfPeople(people)

        # Calculate the distance between the two points
        distance_x = new_center_x - current_x
        distance_y = new_center_y - current_y
        
        # Calculate the number of steps in each exis
        num_steps_x = distance_x // self.step_size
        num_steps_y = distance_y // self.step_size
 
        # Return the number of staps in each axis 
        return (num_steps_x, num_steps_y) 

        