from cryptography.fernet import Fernet
from typing import List, Optional


class SecureChannel:
    """Symmetric encryption channel using Fernet.

    Accepts an optional pre-existing ``key`` so callers can avoid the
    overhead of ``Fernet.generate_key()`` (an OS-entropy read) when
    reconstructing a channel from a known key.
    """

    def __init__(self, key: Optional[bytes] = None):
        self.key = key if key is not None else Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt(self, msg: bytes) -> bytes:
        return self.cipher.encrypt(msg)

    def decrypt(self, token: bytes) -> bytes:
        return self.cipher.decrypt(token)

    def encrypt_batch(self, messages: List[bytes]) -> List[bytes]:
        """Encrypt a list of messages reusing the same cipher instance.

        More efficient than calling ``encrypt()`` in a Python loop because it
        avoids repeated attribute look-ups and call overhead.
        """
        cipher = self.cipher
        return [cipher.encrypt(msg) for msg in messages]

    def decrypt_batch(self, tokens: List[bytes]) -> List[bytes]:
        """Decrypt a list of tokens reusing the same cipher instance."""
        cipher = self.cipher
        return [cipher.decrypt(token) for token in tokens]
