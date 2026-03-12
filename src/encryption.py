from cryptography.fernet import Fernet

class SecureChannel:
    def __init__(self):
        self.encryption_key = Fernet.generate_key()
        self.fernet_cipher = Fernet(self.encryption_key)

    def encrypt(self, plaintext: bytes) -> bytes:
        return self.fernet_cipher.encrypt(plaintext)

    def decrypt(self, encrypted_token: bytes) -> bytes:
        return self.fernet_cipher.decrypt(encrypted_token)
