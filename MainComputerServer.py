from ComputerServer.UdpServer import UdpServer
import numpy as np
from typing import Tuple
from ObjectDetection.EnemyDetectionCv2.EnemyDetection import EnemyDetection
from ObjectDetection.EnemyDetectionCv2.EnemyTargeting import EnemyTargeting
import struct
import cv2
from datetime import datetime

class ImageDetection:
    """
    ImageDetection class ia in charge of the detection of people 
    in frames sent from the raspberrypi
    """
    def __init__(self, server: UdpServer, step_size: int) -> None:
        """
        Initalizing the server in the class
        Args:
            server (Server): server is a Server object that is in charge of sending msgs 
            to the client
            step_size (int): how much is a step
        """
        # Initalizng the server in the class
        self.server = server

        # A bool to check if got frame
        self.got_frame = False

        # The shape of the frame
        self.frame_shape = None

        # The frame it self
        self.frame = None

        # Init the enemy detector
        self.enemy_detector = EnemyDetection()

        # Init enemy targeting
        self.enemy_targeting = EnemyTargeting(step_size)

        # Get width of window
        self.window_width = self.enemy_detector.camera.get(3) 

        # Get height of window
        self.window_height = self.enemy_detector.camera.get(4)

        # Num frames got in evey second
        self.num_frames = 0

        # Start timer to get every second
        self.start = datetime.now()

    def set_shape(self, data: bytes) -> None:
        """
        Get raw data from client, turns it into 
        numpy array shape and sets it to self.frame_shape

        Args:
            data (bytes): Raw data from client
        """

        self.frame_shape = struct.unpack('1i', data)

    def set_frame(self, data: bytes, show_frame: bool = True, show_fps: bool = True) -> None:
        """
        Get raw data from client, turns it into 
        numpy array and sets it to self.frame

        Args:
            data (bytes): Raw data from client
            show_frame (bool): if you want to show frame set true [defualt False]
            show_fps (bool): if you want to show fps set true [defualt False]
        """
                
        # Set frame got from client
        self.frame = cv2.imdecode(np.frombuffer(data, np.uint8).reshape(*self.frame_shape), cv2.IMREAD_COLOR)
        
        # When we want to see the frames we can use show frame
        if show_frame:
            # Shows the frame
            self.enemy_detector.show_frame(self.frame)
        
        if show_fps:
            # Increase the num of frames
            self.num_frames += 1

            # Shows fps
            self.show_fps()
        
    def show_fps(self) -> None:
        """
        Shows the number of frames per second
        """
        # The currnt time
        now = datetime.now()

        # Time past between the start of reciving and now
        time_past = now - self.start

        # Print fps 
        print(f"FPS: {self.num_frames // time_past.seconds}", end = "\r")
        
    def handle_recv(self) -> None:
        """
        In charge of reciving the data from client 
        and retriving correctly
        *** In order for this to work shape has to be sent first ***
        """
        while True:
            code, data, addr = self.server.recv_msg()
            if code == b"SHAPE":
                self.set_shape(data)

            elif code == b"FRAME":
                self.set_frame(data)
                self.send_steps(addr)
    
    def calc_num_steps(self) -> Tuple[int, int]:
        """
        Gets num of steps from current center to person center

        Returns:
            tuple(horizontal, vertical): a tuple that contains num of steps for each diraction
            horizontal (int): if positive to the left if negetive to the right
            vertical (int): if positive down if negetive up
        """
        # Get tuple of person
        person = self.enemy_detector.get_people_from_image(self.frame)

        # Check there is a person
        if person != ():
            # Divide the width and height by 2 
            # in order to get the center of the screen
            return self.enemy_targeting.get_steps_to_people_center(self.window_width // 2, self.window_height // 2, person)
        # If there isnt a person it should'nt move
        return (0, 0)       

    def send_steps(self, addr: tuple) -> None:
        """
        Sends num of steps in each direction
        to raspberryPi

        Args:
            addr (tuple): addres of the client to send to
        """

        # Get num steps
        steps_tuple = self.calc_num_steps()
        
        # Using struct to pack and send the tuple as bytes, len(steps_tuple) 
        # is for the number of elements and i is for their type (integer)
        msg = b'STEPS' + bytearray(struct.pack(f'{len(steps_tuple)}i', *steps_tuple))

        # Send
        self.server.send_msg(msg, addr, False)


if __name__ == "__main__":
    us = UdpServer(8888, 5)
    us.start_server()
    id =ImageDetection(us, 1)
    id.handle_recv()

