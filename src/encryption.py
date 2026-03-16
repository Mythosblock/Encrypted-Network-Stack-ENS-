from cryptography.fernet import Fernet


class SecureChannel:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt(self, msg: bytes) -> bytes:
        return self.cipher.encrypt(msg)

    def decrypt(self, token: bytes) -> bytes:
        return self.cipher.decrypt(token)
