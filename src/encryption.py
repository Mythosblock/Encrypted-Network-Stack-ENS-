from cryptography.fernet import Fernet, InvalidToken


class SecureChannel:
    def __init__(self, key: bytes = None, ttl: int | float | None = None):
        if key is not None:
            if not isinstance(key, (bytes, bytearray)):
                raise TypeError("key must be bytes or bytearray")
            try:
                self.cipher = Fernet(key)
            except Exception:
                raise ValueError("key is not a valid Fernet key")
            self.key = key
        else:
            self.key = Fernet.generate_key()
            self.cipher = Fernet(self.key)
        if ttl is not None and not isinstance(ttl, (int, float)):
            raise TypeError("ttl must be a number")
        self.ttl = ttl

    def encrypt(self, msg: bytes) -> bytes:
        if not isinstance(msg, (bytes, bytearray)):
            raise TypeError("msg must be bytes or bytearray")
        return self.cipher.encrypt(bytes(msg))

    def decrypt(self, token: bytes) -> bytes:
        if not isinstance(token, (bytes, bytearray)):
            raise TypeError("token must be bytes or bytearray")
        try:
            return self.cipher.decrypt(bytes(token), ttl=self.ttl)
        except InvalidToken:
            raise ValueError("token is invalid or has expired")
