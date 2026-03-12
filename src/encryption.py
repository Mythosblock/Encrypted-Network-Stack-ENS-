from typing import Optional

from cryptography.fernet import Fernet, InvalidToken


class SecureChannel:
    """Secure channel for encrypting and decrypting messages using Fernet."""

    def __init__(self, key: Optional[bytes] = None, ttl: Optional[float] = None):
        """Initialize a SecureChannel.

        Args:
            key: Optional Fernet key. If None, a new key is generated.
            ttl: Optional time-to-live in seconds for tokens.

        Raises:
            TypeError: If key is not bytes/bytearray or ttl is not numeric.
            ValueError: If key is invalid or ttl is not positive.
        """
        if ttl is not None:
            if not isinstance(ttl, (int, float)):
                raise TypeError("ttl must be an int or float")
            if ttl <= 0:
                raise ValueError("ttl must be a positive number or None")

        if key is None:
            key = Fernet.generate_key()
        elif not isinstance(key, (bytes, bytearray)):
            raise TypeError("key must be bytes or bytearray")

        key_bytes = bytes(key)

        try:
            cipher = Fernet(key_bytes)
        except (ValueError, TypeError) as exc:
            raise ValueError("key must be a valid Fernet key") from exc

        self.key = key_bytes
        self.ttl = ttl
        self.cipher = cipher

    def encrypt(self, msg: bytes) -> bytes:
        """Encrypt a message.

        Args:
            msg: The message to encrypt (must be bytes or bytearray).

        Returns:
            The encrypted token as bytes.

        Raises:
            TypeError: If msg is not bytes or bytearray.
        """
        if not isinstance(msg, (bytes, bytearray)):
            raise TypeError("msg must be bytes or bytearray")

        return self.cipher.encrypt(bytes(msg))

    def decrypt(self, token: bytes) -> bytes:
        """Decrypt a token.

        Args:
            token: The token to decrypt (must be bytes or bytearray).

        Returns:
            The decrypted message as bytes.

        Raises:
            TypeError: If token is not bytes or bytearray.
            ValueError: If the token is invalid or expired.
        """
        if not isinstance(token, (bytes, bytearray)):
            raise TypeError("token must be bytes or bytearray")

        token_bytes = bytes(token)
        try:
            if self.ttl is None:
                return self.cipher.decrypt(token_bytes)
            return self.cipher.decrypt(token_bytes, ttl=self.ttl)
        except InvalidToken as exc:
            raise ValueError("Invalid or expired token") from exc
