from src.networking import SecureSocket
from src.encryption import SecureChannel

class NetworkNode:
    def __init__(self, node_id="NODE"):
        self.node_id = node_id
        self.socket = SecureSocket()
        self.channel = SecureChannel()

    def _log(self, message: str):
        print(f"[{self.node_id}] {message}")

    def start(self):
        self._log("Node started")

    def send_message(self, msg: bytes):
        token = self.channel.encrypt(msg)
        self._log(f"Sending encrypted: {token}")
        return token

    def receive_message(self, token: bytes):
        msg = self.channel.decrypt(token)
        self._log(f"Received decrypted: {msg}")
        return msg
