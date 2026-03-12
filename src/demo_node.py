import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.node import NetworkNode

node = NetworkNode("DEMO_NODE")
node.start()
token = node.send_message(b"Hello World")
node.receive_message(token)
