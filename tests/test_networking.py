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

    # ------------------------------------------------------------------
    # Input validation
    # ------------------------------------------------------------------

    def test_invalid_host_empty_string(self):
        with self.assertRaises(ValueError):
            SecureSocket(host='')

    def test_invalid_host_non_string(self):
        with self.assertRaises(ValueError):
            SecureSocket(host=12345)

    def test_invalid_port_zero(self):
        with self.assertRaises(ValueError):
            SecureSocket(port=0)

    def test_invalid_port_too_high(self):
        with self.assertRaises(ValueError):
            SecureSocket(port=65536)

    def test_invalid_port_string(self):
        with self.assertRaises(ValueError):
            SecureSocket(port="8000")

    def test_valid_boundary_ports(self):
        low = SecureSocket(port=1)
        self.assertEqual(low.port, 1)
        high = SecureSocket(port=65535)
        self.assertEqual(high.port, 65535)

    # ------------------------------------------------------------------
    # Lazy socket initialisation
    # ------------------------------------------------------------------

    def test_sock_is_none_before_connect(self):
        sock = SecureSocket()
        self.assertIsNone(sock._sock)


if __name__ == "__main__":
    unittest.main()
