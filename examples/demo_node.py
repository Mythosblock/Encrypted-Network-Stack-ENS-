# examples/demo_node.py

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.node import NetworkNode

def main():
    # Create a demo node
    node = NetworkNode(node_id="DEMO_NODE")
    node.start()

    # Send a test message
    message = b"Hello from Demo Node!"
    print("\n[Demo] Sending message...")
    encrypted_token = node.send_message(message)

    # Receive and decrypt the message
    print("\n[Demo] Receiving message...")
    decrypted_message = node.receive_message(encrypted_token)
    print(f"\n[Demo] Decrypted message: {decrypted_message.decode()}")

if __name__ == "__main__":
    main()
