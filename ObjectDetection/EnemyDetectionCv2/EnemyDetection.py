import cv2
import numpy as np
from typing import Tuple
from ObjectDetection.EnemyDetectionCv2.ColorDetection.ColorDetector import ColorDetector

class EnemyDetection:
    """
    EnemyDetection is a class that is in charge
    with everything that has to do with the detection 
    of an enemy
    """

    def __init__(self, video_input:int = 0) -> None:
        """
        Initializng the model and camera in order
        to get them ready fo use
        """

        # Load the pre-trained model for person detection
        self.model = cv2.dnn.readNetFromCaffe('Models\\MobileNetSSD_deploy.prototxt', 'Models\\MobileNetSSD_deploy.caffemodel')

        # Load the video stream
        self.camera = cv2.VideoCapture(video_input)

    def get_image(self) -> np.ndarray:
        """
        Getting image frame from camera
        Returns:
            frame (np.ndarray): the current frame 
        """

        # Read a frame from the video stream
        ret, frame = self.camera.read()
        return frame
    
    def is_wearing_red_shirt(self, person_frame: np.ndarray) -> bool:
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
        lower = np.array([155,25,0])
        upper = np.array([179,255,255])
        
        # Makes mask to test
        mask = cv2.inRange(hsv, lower, upper)

        # Tests with mask and frame
        result = cv2.bitwise_and(person_frame, person_frame, mask=mask)

        # Checks if there is a red shirt
        if np.average(result) > COLOR_THRESHOLD:
            return True

        return False

    def get_people_from_image(self, frame: np.ndarray) -> Tuple:
        """
        Gets people tuple from the image
        Args:
            frame (np.ndarray): the current frame

        Returns:
            Returns:
                people tuple(top left x, top left y, buttom right x, buttom right y, confidence): all the boxes and locations
                of people in the frame 
        """

        # Convert the frame to a blob
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)
        self.model.setInput(blob)

        # Run forward pass to get the detections
        detections = self.model.forward()

        return self.get_people_from_detection(detections, frame)
        
    def get_people_from_detection(self, detections: np.ndarray, frame: np.ndarray) -> Tuple:
        """
        Gets people tulpe from detection
        Args:
            detections (np.ndarray): the detections from the model
            frame (np.ndarray): the current frame
        
        Returns:
            people tuple(top left x, top left y, buttom right x, buttom right y, confidence): all the boxes and locations
            of people in the frame 
        """
        # People lisr
        people_tuple = ()

        # Loop over the detections
        for people in range(detections.shape[2]):
            confidence = detections[0, 0, people, 2]
            if confidence > 0.9:
                # Get the top left x, top left y, buttom right x, buttom right y for the detection
                r_t_x = int(detections[0, 0, people, 3] * frame.shape[1])
                r_t_y = int(detections[0, 0, people, 4] * frame.shape[0])
                l_b_x = int(detections[0, 0, people, 5] * frame.shape[1])
                l_b_y = int(detections[0, 0, people, 6] * frame.shape[0])
                person = frame[r_t_y:l_b_y, r_t_x:l_b_x]
                if ColorDetector.is_domminent(person):
                    people_tuple = (r_t_x, r_t_y, l_b_x, l_b_y, confidence)
                    # The condfidence list is sorted so we want the highest confidence of a red shirt person
                    break
            else:
                # The condfidence list is sorted so if it is lower the 0.9 we want to exit the loop
                break
                
        return people_tuple
    
    

        

