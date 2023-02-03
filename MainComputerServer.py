from ComputerServer.Server import Server
import numpy as np

from ObjectDetection.EnemyDetectionCv2.EnemyDetection import EnemyDetection

class ImageDetection:
    """
    ImageDetection class ia in charge of the detection of people 
    in frames sent from the raspberrypi
    """
    def __init__(self, server: Server) -> None:
        """
        Initalizing the server in the class
        Args:
            server (Server): server is a Server object that is in charge of sending msgs 
            to the client
        """
        # Initalizng the server in the class
        self.server = server

        # Initalizng the client socket from the sockets list in the server
        self.cli_sock = server.client_sockets[0] 

        # A bool to check if got frame
        self.got_frame = False

        # The shape of the frame
        self.frame_shape = None

        # The frame it self
        self.frame = None

        # Init the enemy detector
        self.enemy_detector = EnemyDetection()

    def set_shape(self, data: bytes) -> None:
        """
        Get raw data from client, turns it into 
        numpy array shape and sets it to self.frame_shape

        Args:
            data (bytes): Raw data from client
        """
        self.frame_shape = np.frombuffer(data, dtype=np.int32)

    def set_frame(self, data: bytes) -> None:
        """
        Get raw data from client, turns it into 
        numpy array and sets it to self.frame

        Args:
            data (bytes): Raw data from client
        """
        self.frame = np.frombuffer(data, dtype=np.float32).reshape(*self.frame_shape)

        # In order to stop the while true 
        self.got_frame = True

    def handle_recv(self) -> None:
        """
        In charge of reciving the data from client 
        and retriving correctly
        *** In order for this to work shape has to be sent first ***
        """
        while self.got_frame:
            code, data = self.server.recv_msg(self.cli_sock)
            if code == b"SHAPE":
                self.set_shape(data)

            elif code == b"FRAME":
                self.set_frame(data)
    
    def calc_num_steps(self):
        """
        TODO: complete here and fix branching
        TODO: Add Udp server client
        """
        # Get tuple of person
        self.enemy_detector.get_people_from_image(self.frame)

    def send_steps():
        pass

if __name__ == "__main__":
    sr = Server(1234, 5)
    # sr.start_server()
    id = ImageDetection(sr)
