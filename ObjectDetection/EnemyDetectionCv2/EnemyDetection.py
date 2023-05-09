import cv2
import numpy as np
from typing import Tuple
from ObjectDetection.EnemyDetectionCv2.ColorDetection.ColorDetector import ColorDetector
import os
CONFIDENCE_THRESHOLD: float = 0.8
class EnemyDetection:
    """
    EnemyDetection is a class that is in charge
    with everything that has to do with the detection 
    of an enemy
    """

    def __init__(self, video_input:int = 0, load_models: bool = True) -> None:
        """
        Initializng the model and camera in order
        to get them ready fo use

        Args:
            video_input (int): which input to use
            load_models (bool): if we want to load models
        """

        # Not loading models on the RaspberryPi because it dosent use them 
        if load_models:
            prototext_path = os.path.join('ObjectDetection','EnemyDetectionCv2','Models','MobileNetSSD_deploy.prototxt')
            caffemodel_path = os.path.join('ObjectDetection','EnemyDetectionCv2','Models','MobileNetSSD_deploy.caffemodel')

            # Load the pre-trained model for person detection
            self.model = cv2.dnn.readNetFromCaffe(prototext_path, caffemodel_path)

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
            if confidence > CONFIDENCE_THRESHOLD:
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

    def show_frame(self, frame: np.ndarray) -> None:
        """
        In order to have a graphic and visual
        understanding of the frame

        Args:
            frame (np.ndarray): the current frame to show
        """

        # Show the frame
        cv2.imshow('frame', frame)

        # For the pic to show
        cv2.waitKey(1)
    
    def release_camera(self):
        """
        When done using camera, realse it
        """
        self.camera.release()
    
    

        

