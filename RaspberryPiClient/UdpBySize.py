import socket
from typing import Tuple, ByteString
# Number digits for data size + one delimiter
SIZE_HEADER_FORMAT = "000000000|" 

# Len of size header
LEN_SIZE_HEADER = len(SIZE_HEADER_FORMAT) 

# Bool for debugging
UDP_DEBUG = False 

# Max len to print
LEN_TO_PRINT = 100

# Batch size
BATCH_SIZE = 65536

class UdpBySize:

    @staticmethod
    def recv_by_size(sock: socket.socket) -> Tuple[ByteString, Tuple]:
        """
        Recives data by size
        Args:
            sock (socket.socket): socket to recv from

        Returns:
            data (bytearray): the data recived [if '' there was an error while reciving]
            addr (tuple): the addr of the sender 
        """
        data_len = 0
        size_header = b''
        data  = b''
        addr = b''

        # Get data length 
        while len(size_header) < LEN_SIZE_HEADER:
            recved = sock.recvfrom(LEN_SIZE_HEADER - len(size_header))
            _s = recved[0]
            addr = recved[1]
            if _s == b'':
                return b'', addr
            size_header += _s
        
        # Get data 
        if size_header != b'':
            data_len = int(size_header[:LEN_SIZE_HEADER - 1])
            while len(data) < data_len:
                _d = sock.recvfrom(data_len - len(data))[0]
                if _d == b'':
                    return b'', addr
                data += _d

        # Debugging
        if  UDP_DEBUG and size_header != b'':
            print ("\nRecv(%s)>>>" % (size_header, ), end='')
            print ("%s"%(data[:min(len(data), LEN_TO_PRINT)], ))

        # If got Partial data returns nothing becuase partial data is like no data
        if data_len != len(data):
            return b'', addr

        # Returnd data recived without length
        return data, addr

    @staticmethod
    def send_with_size(sock: socket.socket, bdata: bytearray, addr: bytearray) -> None:
        """
        Recives data by size
        Args:
            sock (socket.socket): socket to send to
            bdata (bytearray): data to send to socket
            addr (bytearray): the addr to send to
        """

        # Get length of data
        len_data = len(bdata)
        header_data = (str(len(bdata)).zfill(LEN_SIZE_HEADER - 1) + "|").encode()

        # Send length first
        sock.sendto(header_data, addr)

        # Check if it is a big file
        if len_data > 1000:
            
            # Split to batches
            for batch_num in range(0, len_data, BATCH_SIZE):
                # Send to server
                sock.sendto(bdata[batch_num:batch_num+BATCH_SIZE], addr)

        else:
            # Send data after
            sock.sendto(bdata, addr)

        # Checking approvel from server
        # if sock.recvfrom(2)[0] == b"OK":
        #     pass  

        # Debugging
        if UDP_DEBUG and  len_data > 0:
            print ("\nSent(%s)>>>" % (len_data, ), end='')
            print ("%s"%(bdata[:min(len(bdata), LEN_TO_PRINT)],))
