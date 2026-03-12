import logging

from src.networking import SecureSocket
from src.encryption import SecureChannel

logger = logging.getLogger(__name__)


class NetworkNode:
    """Network node that integrates SecureSocket and SecureChannel.

    Uses ``logging`` instead of ``print()`` so that message-level output
    carries zero I/O cost when the caller has not configured a handler
    (the default ``logging.lastResort`` level is WARNING, so DEBUG messages
    are silently discarded without any blocking write).
    """

    def __init__(self, node_id: str = "NODE"):
        self.node_id = node_id
        self.socket = SecureSocket()
        self.channel = SecureChannel()

    def start(self):
        logger.info("[%s] Node started", self.node_id)

    def send_message(self, msg: bytes) -> bytes:
        token = self.channel.encrypt(msg)
        logger.debug("[%s] Sending encrypted: %s", self.node_id, token)
        return token

    def receive_message(self, token: bytes) -> bytes:
        msg = self.channel.decrypt(token)
        logger.debug("[%s] Received decrypted: %s", self.node_id, msg)
        return msg
