import rsa

class RSAEncryption:
    KEYS_LEN = 512
    
    def __init__(self) -> None:
        self.__generate_keys()

    def __generate_keys(self) -> None:
        """
        Creates a set of keys: public and private
        """
        self.public_key, self.__private_key = rsa.newkeys(self.KEYS_LEN)

    @staticmethod
    def encrypt_rsa(public_key: rsa.PublicKey, message: str) -> bytes:
        """
        Encrypts message with the friends public key
        Args:
            public_key: (rsa.PublicKey) - other client/server public key
            message: (str) - the messge i want to encrypt
        Retuns:
            encrypted_msg: (str) - the messge i want to send encrypted
        """
        return rsa.encrypt(message.encode(), public_key)

    def decrypt_rsa(self, message: bytes) -> str:
        """
        Encrypts message with the friends public key
        Args:
            public_key: (rsa.PublicKey) - other client/server public key
            message: (str) - the messge i want to encrypt
        Retuns:
            encrypted_msg: (str) - the messge i want to send encrypted
        """
        return rsa.decrypt(message, self.__private_key).decode()
