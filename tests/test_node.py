import logging
import unittest
from src.node import NetworkNode


class TestNetworkNode(unittest.TestCase):
    def test_send_receive_round_trip(self):
        node = NetworkNode()
        msg = b"hello world"
        token = node.send_message(msg)
        result = node.receive_message(token)
        self.assertEqual(result, msg)

    def test_send_message_returns_bytes(self):
        node = NetworkNode()
        token = node.send_message(b"data")
        self.assertIsInstance(token, bytes)

    def test_start_logs_info(self):
        node = NetworkNode(node_id="TEST")
        with self.assertLogs("src.node", level=logging.INFO):
            node.start()

    def test_send_message_logs_debug(self):
        node = NetworkNode(node_id="TEST")
        with self.assertLogs("src.node", level=logging.DEBUG):
            node.send_message(b"ping")

    def test_receive_message_logs_debug(self):
        node = NetworkNode(node_id="TEST")
        token = node.send_message(b"ping")
        with self.assertLogs("src.node", level=logging.DEBUG):
            node.receive_message(token)


if __name__ == "__main__":
    unittest.main()
