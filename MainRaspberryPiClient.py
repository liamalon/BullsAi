
from RaspberryPiClient.UdpClient import UdpClient
from ObjectDetection.EnemyDetectionCv2.EnemyDetection import EnemyDetection
import numpy as np
import struct
import sys

class ImageTransfer:
    """
    ImageTransfer is in charge of capturing frames
    and sending them to the server 
    """

    def __init__(self, udp_client: UdpClient) -> None:
        """
        Intializg UdpClient class and EnemyDetection class 
        """
        self.enemy_detector = EnemyDetection(load_models=False)
        self.udp_client = udp_client

    def send_frame(self) -> None:
        """
        Sending the frame to the server on the computer
        """
        frame = self.enemy_detector.get_image()
        self.send_shape(frame.shape)

        self.udp_client.send_msg(b'FRAME'+frame.tobytes(), False)
    
    def send_shape(self, shape: tuple) -> None:
        """
        Sends the shape of the frame to the server on the computer
        """

        # Using struct to pack and send the tuple as bytes, len(shape) 
        # is for the number of elements and i is for their type (integer)
        self.udp_client.send_msg(b'SHAPE'+bytearray(struct.pack(f'{len(shape)}i', *shape)), False)

    def recv_steps(self, data: bytearray):
        steps = struct.unpack('2i', data)
        print(steps)
    
    def handle_server(self):
        while True:
            self.send_frame()
            code, data, addr = self.udp_client.recv_msg()

            if code == b"STEPS":
                self.recv_steps(data)

if __name__ == "__main__":
    udp_client = UdpClient(sys.argv[1], 8888, 5)
    it = ImageTransfer(udp_client)
    it.handle_server()