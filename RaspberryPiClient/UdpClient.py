import socket
from RaspberryPiClient.UdpBySize import UdpBySize
from typing import Any, Tuple, ByteString
import numpy as np

# Defualt listen ip
DEFUALT_LISTEN_IP = '0.0.0.0'

# Batch size
BUFF_SIZE = 65536

class UdpClient:
    """
    UdpServer is a class that is in charge 
    with everuthing that has to do with 
    the server side in the networking 
    """

    def __init__(self, server_ip: str, port:int, msg_code_len:int) -> None:
        """
        Inits varibals in server
        Args:
            server_ip (str): gets the ip of the server 
            port (int): gets the port to open the server on 
            msg_code_len (int): the len of the msg code
        """
        # The port of the server
        self.port = port

        # The ip of the server
        self.server_ip = server_ip

        # Create socket
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        
        # Set socket opt
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        
        # Set msg code len
        self.msg_code_len = msg_code_len
                
    def send_msg(self, data: Any, to_encode:bool = False) -> None:
        """
        Sends data to client
        Args:
            data (Any): can be str or bytes, the data you want to send
            addr (tuple): the addr to send to
            to_encode (bool): set to false, if true will encode msg
        """
        # If we want to encode
        if to_encode:
            # Encoed the data
            data = data.encode()

        # Send data with size
        UdpBySize.send_with_size(self.socket, data, (self.server_ip, self.port))
    
    def recv_msg(self) -> Tuple[ByteString, ByteString, Tuple]:
        """
        Recives data from client
        Args:
            sock (socket.socket): socket to recive data from

        Returns:
            (code: bytes , data: bytes, address: tuple): the msg code and msg data and addr of the sender
        """
        # Reciving data and breaking it down to message and address
        message, address = UdpBySize.recv_by_size(self.socket)

        # The first X (self.msg_code_len) bytes is code
        code = message[:self.msg_code_len]

        # The rest is data itself
        data = message[self.msg_code_len:]
        
        return code, data, address

    def send_frame(self, frame: np.ndarray):
        """
        Sends frame to server 
        """
        self.socket.sendto(frame, (self.server_ip, self.port))

    def flush_sock_buff(self) -> None:
        """
        Flushes the socket buff when changing between modes
        """
        while True:
            try:
                self.socket.settimeout(1)
                print("Here")
                self.socket.recvfrom(BUFF_SIZE)
            except socket.timeout:
                '''
                When it reaches here it means there is no data in buff
                '''
                return