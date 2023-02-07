
from RaspberryPiClient.UdpClient import UdpClient
from ObjectDetection.EnemyDetectionCv2.EnemyDetection import EnemyDetection
import numpy as np
import struct
import sys
import cv2

FRAME_QUALITY = 15

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
    
    def decode_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        In order to send less bytes and get 
        faster results we decode the frame and compress it

        Args:
            frame (np.ndarray): the frame to decode
        """
        _, buffer = cv2.imencode('.jpg', frame, self.params)
        return buffer

    def send_frame(self) -> None:
        """
        Sending the frame to the server on the computer
        """
        frame = self.decode_frame(self.enemy_detector.get_image())
        self.send_shape(frame.shape)

        self.udp_client.send_msg(b'FRAME'+ frame.tobytes(), False)
    
    def send_shape(self, shape: tuple) -> None:
        """
        Sends the shape of the frame to the server on the computer
        """
        # Using struct to pack and send the tuple as bytes, len(shape) 
        # is for the number of elements and i is for their type (integer)
        self.udp_client.send_msg(b'SHAPE'+bytearray(struct.pack(f'{len(shape)}i', *shape)), False)

    def recv_steps(self, data: bytearray) -> None:
        """
        Recive number of steps from client

        Args:
            data (bytearray): the date from server
        """
        # Need to unpack in order to get the steps tuple
        steps = struct.unpack('2i', data)

        # Debugging
        print("Num steps:", steps, end ="\r")
    
    def handle_server(self) -> None:
        """
        Handles networking with server
        """
        while True:
            self.send_frame()
            code, data, addr = self.udp_client.recv_msg()

            if code == b"STEPS":
                self.recv_steps(data)

if __name__ == "__main__":
    udp_client = UdpClient(sys.argv[1], 8888, 5)
    it = ImageTransfer(udp_client, video_input=0)
    it.handle_server()