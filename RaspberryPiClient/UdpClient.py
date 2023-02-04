import socket
from RaspberryPiClient.UdpBySize import UdpBySize
from typing import Any, Tuple, ByteString

DEFUALT_LISTEN_IP = '0.0.0.0'

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
        self.port = port
        self.server_ip = server_ip
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.msg_code_len = msg_code_len
                
    def send_msg(self, data: Any, to_encode:bool = False) -> None:
        """
        Sends data to client
        Args:
            data (Any): can be str or bytes, the data you want to send
            addr (tuple): the addr to send to
            to_encode (bool): set to false, if true will encode msg
        """
        if to_encode:
            data = data.encode()

        UdpBySize.send_with_size(self.socket, data, (self.server_ip, self.port))
    
    def recv_msg(self) -> Tuple[ByteString, ByteString, Tuple]:
        """
        Recives data from client
        Args:
            sock (socket.socket): socket to recive data from

        Returns:
            (code: bytes , data: bytes, address: tuple): the msg code and msg data and addr of the sender
        """

        message, address = UdpBySize.recv_by_size(self.socket)
        code = message[:self.msg_code_len]
        data = message[self.msg_code_len:]
        
        return code, data, address

