from src.networking import SecureSocket
from src.encryption import SecureChannel

class NetworkNode:
    def __init__(self, node_id="NODE"):
        self.node_id = node_id
        self.socket = SecureSocket()
        self.channel = SecureChannel()

    def start(self):
        print(f"[{self.node_id}] Node started")

    def send_message(self, msg: bytes):
        token = self.channel.encrypt(msg)
        print(f"[{self.node_id}] Sending encrypted: {token}")
        return token

    def receive_message(self, token: bytes):
        msg = self.channel.decrypt(token)
        print(f"[{self.node_id}] Received decrypted: {msg}")
        return msg
