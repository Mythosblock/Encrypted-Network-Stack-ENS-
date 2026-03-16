from __future__ import annotations

import logging

from src.networking import SecureSocket
from src.encryption import SecureChannel

logger = logging.getLogger(__name__)


class NetworkNode:
    """A network node that combines encrypted messaging with socket I/O.

    Performance notes
    -----------------
    * Uses :mod:`logging` instead of ``print`` so that log output can be
      suppressed, redirected, or filtered without touching the call sites.
      ``print`` bypasses Python's logging infrastructure and always writes
      to stdout, making it unsuitable for production use.
    """

    def __init__(self, node_id: str = "NODE") -> None:
        self.node_id = node_id
        self.socket = SecureSocket()
        self.channel = SecureChannel()

    def start(self) -> None:
        logger.info("[%s] Node started", self.node_id)

    def send_message(self, msg: bytes) -> bytes:
        token = self.channel.encrypt(msg)
        logger.debug("[%s] Sending encrypted: %s", self.node_id, token)
        return token

    def receive_message(self, token: bytes) -> bytes:
        msg = self.channel.decrypt(token)
        logger.debug("[%s] Received decrypted: %s", self.node_id, msg)
        return msg
