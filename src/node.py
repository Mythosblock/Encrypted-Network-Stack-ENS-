from src.networking import SecureSocket
from src.encryption import SecureChannel

class NetworkNode:
    def __init__(self, node_id="NODE"):
        self.node_id = node_id
        self.socket = SecureSocket()
        self.channel = SecureChannel()

    def start(self):
        print(f"[{self.node_id}] Node started")

    def send_message(self, plaintext_message: bytes):
        encrypted_token = self.channel.encrypt(plaintext_message)
        print(f"[{self.node_id}] Sending encrypted: {encrypted_token}")
        return encrypted_token

    def receive_message(self, encrypted_token: bytes):
        decrypted_message = self.channel.decrypt(encrypted_token)
        print(f"[{self.node_id}] Received decrypted: {decrypted_message}")
        return decrypted_message
