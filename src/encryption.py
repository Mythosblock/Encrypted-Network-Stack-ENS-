from cryptography.fernet import Fernet, InvalidToken

class SecureChannel:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt(self, msg: bytes) -> bytes:
        if not isinstance(msg, (bytes, bytearray)):
            raise TypeError("Message must be bytes")
        return self.cipher.encrypt(msg)

    def decrypt(self, token: bytes) -> bytes:
        if not isinstance(token, (bytes, bytearray)):
            raise TypeError("Token must be bytes")
        try:
            return self.cipher.decrypt(token)
        except InvalidToken as exc:
            raise ValueError("Invalid token") from exc
