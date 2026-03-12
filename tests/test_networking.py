import unittest
from src.networking import SecureSocket


class TestNetworking(unittest.TestCase):
    def test_socket_creation(self):
        sock = SecureSocket()
        self.assertEqual(sock.host, '127.0.0.1')
        self.assertEqual(sock.port, 8000)

    def test_socket_custom_host_port(self):
        sock = SecureSocket(host='0.0.0.0', port=9000)
        self.assertEqual(sock.host, '0.0.0.0')
        self.assertEqual(sock.port, 9000)


if __name__ == "__main__":
    unittest.main()
