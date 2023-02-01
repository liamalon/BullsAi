import socket
from TcpBySize import TcpBySize
from typing import Any

DEFUALT_LISTEN_IP = '0.0.0.0'
DEFUALT_LISTEN_NUM = 20

class Server:
    """
    Server is a class that is in charge 
    with everuthing that has to do with 
    the server side in the networking 
    """
    def __init__(self, port:int, msg_code_len:int) -> None:
        """
        Inits varibals in server
        Args:
            port (int): gets the port the to open the server on 
            msg_code_len (int): the len of the msg code
        """
        self.port = port
        self.server_sock = socket.socket()
        self.client_sockets = []
        self.msg_code_len = msg_code_len
    
    def start_listen(self) -> None:
        """
        Opens the server to listen
        Args: 
            None
        """
        self.server_sock.bind((DEFUALT_LISTEN_IP, self.port))
        self.server_sock.listen(DEFUALT_LISTEN_NUM)
    
    
    def accept_clients(self):
        """
        Accepts clients to server
        """
        cli_sock, addr = self.server_sock.accept()
        self.client_sockets.append(cli_sock)
        print(f"connected, ip {addr}, port {self.port}")
    
    def start_server(self):
        """
        Starts server listen and accept
        """
        self.start_listen()
        self.accept_clients()
    
    def send_msg(self, sock: socket.socket, data: Any):
        """
        Sends data to client
        Args:
            sock (socket.socket): socket to send the data to
            data (Any): can be str or bytes, the data you want to send
        """
        if not isinstance(data, bytes):
            data = data.encode()

        TcpBySize.send_with_size(sock, data)
    
    def recv_msg(self, sock: socket.socket):
        """
        Recives data from client
        Args:
            sock (socket.socket): socket to recive data from

        Returns:
            (code: bytes , data: bytes): the msg code and msg data 
        """
        recved_data = TcpBySize.recv_by_size(sock)

        code = recved_data[:self.msg_code_len]
        data = recved_data[self.msg_code_len:]

        return (code, data)
