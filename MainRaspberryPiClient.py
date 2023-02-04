
from RaspberryPiClient.UdpClient import UdpClient



if __name__ == "__main__":
    uc = UdpClient("127.0.0.1", 8888, 4)
    uc.send_msg("Hey", True)
    code, msg, addt = uc.recv_msg()
    print(code, msg)