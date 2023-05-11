from ComputerServer.UdpServer import UdpServer
import numpy as np
from typing import Tuple
from ObjectDetection.EnemyDetectionCv2.EnemyDetection import EnemyDetection
from ObjectDetection.EnemyDetectionCv2.EnemyTargeting import EnemyTargeting
from Security.Encryption import RSAEncryption
import struct
import cv2
import time

FPS_BATCH: int = 20
ORIGINNAL_NUM_FRAMES_TO_DETECT: int = 1
NUM_FRAMES_TO_DETECT: int = ORIGINNAL_NUM_FRAMES_TO_DETECT
NUM_FRAMES_TO_DETECT_TO_FIRE: int = 60
STEP_SIZE_THRESHOLD: int = 15 
AUTO_SIZE_FIXER: int = 1

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
        self.start = time.time()

        # Indicates if the server is running or not
        self.running = True

        # Current client addr
        self.addr = None

        # Exit connection or not
        self.exit = False
        
        # Red shirt man bounding
        self.person_bounding = (0, 0, 0, 0, 0)

        self.rsa_encryption = RSAEncryption()

    def set_frame(self, data: bytes, show_frame: bool = False, show_fps: bool = False) -> None:
        """
        Get raw data from client, turns it into 
        numpy array and sets it to self.frame

        Args:
            data (bytes): Raw data from client
            show_frame (bool): if you want to show frame set true [defualt False]
            show_fps (bool): if you want to show fps set true [defualt False]
        """
                
        # Set frame got from client
        self.frame = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), 1)

        # When we want to see the frames we can use show frame
        if show_frame:
            # Shows the frame
            self.enemy_detector.show_frame(self.frame)

        # Increase the num of frames
        self.num_frames += 1
        
        if show_fps:
            # Shows fps
            self.show_fps()
        
    def show_fps(self) -> None:
        """
        Shows the number of frames per second
        """
        # Check if time to print fps
        if self.num_frames % FPS_BATCH == 0:
            # The currnt time
            now = time.time()

            # Time past between the start of reciving and now
            time_past = now - self.start

            # Print fps 
            print(f"FPS: {self.num_frames // time_past}", end = "\r")

            # Reseting num frames to 0
            self.num_frames = 0

            # Reseting the time start to now
            self.start = time.time()
            
    def handle_recv(self) -> None:
        """
        In charge of reciving the data from client 
        and retriving correctly
        *** In order for this to work shape has to be sent first ***
        """
        while self.running:
            data, addr = self.server.recv_frame()
            self.addr = addr
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
            self.person_bounding = person
            return self.enemy_targeting.get_steps_to_people_center(self.window_width // 2, self.window_height // 2, person)
        self.person_bounding = (0, 0, 0, 0, 0)
        # If there isnt a person it should'nt move
        return (0, 0)       
    
    def steps_thresholding(self, steps_tuple: tuple) -> tuple:
        """
        Inorder to avoid small steps we filter out any step lower
        then a certin threshold {STEP_SIZE_THRESHOLD}
        Args:
            steps_tuple: (tuple) - steps tuple, (x_steps, y_steps)
        Returns:
            filtered_steps_tuple: (tuple) - steps tuple, (x_steps, y_steps)
        """
        x_steps = 0 if abs(steps_tuple[0]) < STEP_SIZE_THRESHOLD else steps_tuple[0]
        y_steps = 0 if abs(steps_tuple[1]) < STEP_SIZE_THRESHOLD else steps_tuple[1]
        
        return (x_steps, y_steps)

    def send_steps(self, addr: tuple, steps_tuple: tuple = None) -> None:
        """
        Sends num of steps in each direction
        to raspberryPi

        Args:
            addr (tuple): addres of the client to send to
            steps_tuple (tuple): num of steps, is none by defualt
        """
        if self.exit:
            self.__send_exit()
            return
        
        if not (self.num_frames % (NUM_FRAMES_TO_DETECT * NUM_FRAMES_TO_DETECT_TO_FIRE)):            
            if steps_tuple is None:
                # Get num steps
                steps_tuple = self.calc_num_steps()

            # Threshold steps tuple
            steps_tuple = self.steps_thresholding(steps_tuple)

            steps_tuple = (int(steps_tuple[0] * AUTO_SIZE_FIXER), int(steps_tuple[1] * AUTO_SIZE_FIXER))

            # Using struct to pack and send the tuple as bytes, len(steps_tuple) 
            # is for the number of elements and i is for their type (integer)
            msg = b'FIREG' + bytearray(struct.pack(f'{len(steps_tuple)}i', *steps_tuple))

            # Send
            self.server.send_msg(msg, addr, False)

        # Check if time to send ai detection
        elif not (self.num_frames % NUM_FRAMES_TO_DETECT):
            if steps_tuple is None:
                # Get num steps
                steps_tuple = self.calc_num_steps()

            # Threshold steps tuple
            steps_tuple = self.steps_thresholding(steps_tuple)

            steps_tuple = (int(steps_tuple[0] * AUTO_SIZE_FIXER), int(steps_tuple[1] * AUTO_SIZE_FIXER))

            # Using struct to pack and send the tuple as bytes, len(steps_tuple) 
            # is for the number of elements and i is for their type (integer)
            msg = b'STEPS' + bytearray(struct.pack(f'{len(steps_tuple)}i', *steps_tuple))

            # Send
            self.server.send_msg(msg, addr, False)
    
    def send_fire(self, addr: tuple) -> None:
        """
        Sends fire to the client

        Args:
            addr (tuple): addres of the client to send to
        """
        msg = b'FIREG' + bytearray(struct.pack(f'{len((0, 0))}i', *(0, 0)))

        # Send
        self.server.send_msg(msg, addr, False)
    
    def send_exit(self) -> None:
        """
        Sets exit to true in order to exit in the next round 
        """
        self.exit = True
    
    def __send_exit(self) -> None:
        """
        Sends exit to the client
        """

        self.running = False
        
        msg = b'EXITC' 

        # Reset num steps
        self.num_frames = 0

        # Send
        self.server.send_msg(msg, self.addr, False)

        self.exit = False
    
    def force_exit(self):
        """
        Force sending exit to client
        """
        self.__send_exit()

    def handshake(self) -> None:
        """
        Handshake to start communication
        """
        print("Waiting for RSA public key")
        code, data, addr = self.server.recv_msg()

        msg = "HNDSH"+str(NUM_FRAMES_TO_DETECT)

        encrypted_msg  = self.rsa_encryption.encrypt_rsa(data, msg)

        print("Sending encrypted msg")
        self.server.send_msg(encrypted_msg, addr, False)

    def change_frame_rate(self, new_frame_rate: int = ORIGINNAL_NUM_FRAMES_TO_DETECT):
        """
        Changes num of frames to send steps after ai anlasys
        Args:
            new_frame_rate: (int) - new frame rate
        """
        global NUM_FRAMES_TO_DETECT
        NUM_FRAMES_TO_DETECT = new_frame_rate

