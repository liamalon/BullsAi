import socket

# Number digits for data size + one delimiter
SIZE_HEADER_FORMAT = "000000000|" 

# Len of size header
LEN_SIZE_HEADER = len(SIZE_HEADER_FORMAT) 

# Bool for debugging
TCP_DEBUG = False 

# Max len to print
LEN_TO_PRINT = 100 

class TcpBySize:

    @staticmethod
    def recv_by_size(sock: socket.socket) -> bytearray:
        """
        Recives data by size
        Args:
            sock (socket.socket): socket to recv from

        Returns:
            data (bytearray): the data recived [if '' there was an error while reciving]
        """
        data_len = 0
        size_header = b''
        data  = b''

        # Get data length 
        while len(size_header) < LEN_SIZE_HEADER:
            _s = sock.recv(LEN_SIZE_HEADER - len(size_header))
            if _s == b'':
                return b''
            size_header += _s
        
        # Get data 
        if size_header != b'':
            data_len = int(size_header[:LEN_SIZE_HEADER - 1])
            while len(data) < data_len:
                _d = sock.recv(data_len - len(data))
                if _d == b'':
                    return b''
                data += _d

        # Debugging
        if  TCP_DEBUG and size_header != b'':
            print ("\nRecv(%s)>>>" % (size_header, ), end='')
            print ("%s"%(data[:min(len(data), LEN_TO_PRINT)], ))

        # If got Partial data returns nothing becuase partial data is like no data
        if data_len != len(data):
            return b''

        # Returnd data recived without length
        return data

    @staticmethod
    def send_with_size(sock: socket.socket, bdata: bytearray) -> None:
        """
        Recives data by size
        Args:
            sock (socket.socket): socket to send to
            bdata (bytearray): data to send to socket
        """

        # Get length of data
        len_data = len(bdata)
        header_data = str(len(bdata)).zfill(LEN_SIZE_HEADER - 1) + "|"

        # Add length and original data
        bytea = bytearray(header_data,encoding='utf8') + bdata

        # Send data
        sock.send(bytea)

        # Debugging
        if TCP_DEBUG and  len_data > 0:
            print ("\nSent(%s)>>>" % (len_data, ), end='')
            print ("%s"%(bytea[:min(len(bytea), LEN_TO_PRINT)],))
