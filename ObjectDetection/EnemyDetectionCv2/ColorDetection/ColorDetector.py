import numpy as np
import cv2

COLOR_THRESHOLD = 12

LOWER_RED = [155,25,0]

UPPER_RED = [179,255,255]

class ColorDetector:

    @staticmethod
    def is_domminent(person_frame: np.ndarray):
        """
        Checks if the person in the frame is wearing a red shirt
        Args:
            person_frame (np.ndarray): the frame only of the person
        
        Returns:
            bool: True if hw is wearing a red shirt, False if not
        """

        # Check if person frame is empty
        if not np.any(person_frame):
            return False

        # Convert to hsv color
        hsv = cv2.cvtColor(person_frame, cv2.COLOR_BGR2HSV)

        # lower and upper red in hsv
        lower = np.array(LOWER_RED)
        upper = np.array(UPPER_RED)
        
        # Makes mask to test
        mask = cv2.inRange(hsv, lower, upper)

        # Tests with mask and frame
        result = cv2.bitwise_and(person_frame, person_frame, mask=mask)

        # Checks if there is a red shirt
        if np.average(result) > COLOR_THRESHOLD:
            return True

        return False