from __future__ import annotations

from cryptography.fernet import Fernet, InvalidToken


class SecureChannel:
    """Symmetric encryption channel backed by Fernet.

    Performance notes
    -----------------
    * Pass an existing *key* to reuse a channel without paying the cost of
      cryptographic key generation (``Fernet.generate_key`` calls
      ``os.urandom`` internally).
    * Use :meth:`encrypt_batch` / :meth:`decrypt_batch` instead of looping
      over :meth:`encrypt` / :meth:`decrypt` to avoid repeated Python-level
      attribute lookups and function-call overhead.
    """

    def __init__(self, key: bytes | bytearray | None = None) -> None:
        if key is not None:
            if not isinstance(key, (bytes, bytearray)):
                raise TypeError("key must be bytes or bytearray")
            self.key: bytes = bytes(key)
        else:
            self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    # ------------------------------------------------------------------
    # Single-message helpers
    # ------------------------------------------------------------------

    def encrypt(self, msg: bytes | bytearray) -> bytes:
        """Encrypt *msg* and return the Fernet token."""
        if not isinstance(msg, (bytes, bytearray)):
            raise TypeError("msg must be bytes or bytearray")
        return self.cipher.encrypt(bytes(msg))

    def decrypt(self, token: bytes | bytearray, ttl: int | float | None = None) -> bytes:
        """Decrypt *token* and return the original plaintext.

        Parameters
        ----------
        token:
            Fernet token produced by :meth:`encrypt`.
        ttl:
            Optional maximum age of the token in seconds.  Expired tokens
            raise :exc:`ValueError`.
        """
        if not isinstance(token, (bytes, bytearray)):
            raise TypeError("token must be bytes or bytearray")
        try:
            kwargs = {} if ttl is None else {"ttl": int(ttl)}
            return self.cipher.decrypt(bytes(token), **kwargs)
        except InvalidToken as exc:
            raise ValueError("invalid or expired token") from exc

    # ------------------------------------------------------------------
    # Batch helpers — avoid per-call overhead when processing many messages
    # ------------------------------------------------------------------

    def encrypt_batch(self, messages: list[bytes | bytearray]) -> list[bytes]:
        """Encrypt a list of messages, returning a list of Fernet tokens.

        More efficient than calling :meth:`encrypt` in a loop because the
        cipher object is looked up only once.
        """
        if not isinstance(messages, list):
            raise TypeError("messages must be a list")
        for i, m in enumerate(messages):
            if not isinstance(m, (bytes, bytearray)):
                raise TypeError(f"messages[{i}] must be bytes or bytearray")
        _encrypt = self.cipher.encrypt
        return [_encrypt(bytes(m)) for m in messages]

    def decrypt_batch(
        self,
        tokens: list[bytes | bytearray],
        ttl: int | float | None = None,
    ) -> list[bytes]:
        """Decrypt a list of Fernet tokens, returning a list of plaintexts.

        More efficient than calling :meth:`decrypt` in a loop because the
        cipher object is looked up only once.
        """
        if not isinstance(tokens, list):
            raise TypeError("tokens must be a list")
        for i, t in enumerate(tokens):
            if not isinstance(t, (bytes, bytearray)):
                raise TypeError(f"tokens[{i}] must be bytes or bytearray")
        _decrypt = self.cipher.decrypt
        kwargs = {} if ttl is None else {"ttl": int(ttl)}
        try:
            return [_decrypt(bytes(t), **kwargs) for t in tokens]
        except InvalidToken as exc:
            raise ValueError("invalid or expired token") from exc
