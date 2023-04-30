
import threading
from RaspberryPiClient.UdpClient import UdpClient
from ObjectDetection.EnemyDetectionCv2.EnemyDetection import EnemyDetection
from MotorDriver.MotorsDriver import MotorsDriver
from GunHandler.GunHandler import Gun
import numpy as np
import struct
import sys
import cv2

FRAME_QUALITY = 15
NUM_FRAMES_TO_DETECT = 10

class ImageTransfer:
    """
    ImageTransfer is in charge of capturing frames
    and sending them to the server 
    """

    def __init__(self, udp_client: UdpClient, video_input: int = 0) -> None:
        """
        Intializg UdpClient class and EnemyDetection class 
        Args:
            udp_client (UdpClient): the udp client of the rsapberrypi
            video_input (int): the video input you want to use 
        """
        self.enemy_detector = EnemyDetection(load_models=False, video_input=video_input)
        self.udp_client = udp_client
        self.params = [cv2.IMWRITE_JPEG_QUALITY, FRAME_QUALITY]
        self.num_frames = 0
        self.motors_driver = MotorsDriver()
        self.gun = Gun()
        self.gun_thread = None
        self.run = True
    
    def encode_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        In order to send less bytes and get 
        faster results we encode the frame and compress it

        Args:
            frame (np.ndarray): the frame to decode
        """
        _, buffer = cv2.imencode('.jpg', frame, self.params)
        return buffer

    def send_frame(self) -> None:
        """
        Sending the frame to the server on the computer
        """
        frame = self.encode_frame(self.enemy_detector.get_image())

        self.udp_client.send_frame(frame)

        self.num_frames += 1
    
    def recv_steps(self, data: bytearray) -> None:
        """
        Recive number of steps from client

        Args:
            data (bytearray): the date from server
        """
        # Need to unpack in order to get the steps tuple
        self.steps = struct.unpack('2i', data)

        # Debugging
        print("Num steps:", self.steps, "\t", end ="\r")

    def move_motors(self) -> None:
        """
        Move the motors async to avoid lags with camera
        Args:
            None
        
        Returns:
            None
        """
        while self.run:
            if self.steps != (0, 0):
                self.motors_driver.move_motors(self.steps)
            self.steps = (0, 0)

    def fire(self):
        """
        Fires the gun
        """
        self.gun_thread = threading.Thread(target=self.gun.fire)
        self.gun_thread.start()
    
    def handle_server(self) -> None:
        """
        Handles networking with server
        """
        motors_thread = threading.Thread(self.move_motors)
        motors_thread.start()

        while self.run:
            # Send frame to server
            self.send_frame()

            # Check if it is a time to get ai detection
            if not (self.num_frames % NUM_FRAMES_TO_DETECT):

                # Recv detection from server
                code, data, addr = self.udp_client.recv_msg()

                # Check if msg code is steps
                if code == b"STEPS":

                    # Recv steps
                    self.recv_steps(data)

                elif code == b"FIREG":
                    if self.gun_thread is not None:
                        self.gun_thread.join()
                    self.recv_steps(data)
                    self.fire()
                    
        # Avoid thread zombies 
        motors_thread.join()

if __name__ == "__main__":
    udp_client = UdpClient(sys.argv[1], 8888, 5)
    it = ImageTransfer(udp_client, video_input = 0)
    it.handle_server() 