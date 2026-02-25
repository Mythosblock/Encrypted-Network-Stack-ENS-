import unittest
from src.networking import SecureSocket

class TestNetworking(unittest.TestCase):
    def test_connect(self):
        sock = SecureSocket()
        self.assertEqual(sock.host, '127.0.0.1')
        self.assertEqual(sock.port, 8000)

if __name__ == "__main__":
    unittest.main()
