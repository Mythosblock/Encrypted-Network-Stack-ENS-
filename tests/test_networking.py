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

    # --- Lazy socket init ---
    def test_sock_initially_none(self):
        sock = SecureSocket()
        self.assertIsNone(sock._sock)

    # --- Host validation ---
    def test_empty_host_raises_value_error(self):
        with self.assertRaises(ValueError):
            SecureSocket(host='', port=8000)

    def test_non_string_host_raises_value_error(self):
        with self.assertRaises(ValueError):
            SecureSocket(host=123, port=8000)

    def test_none_host_raises_value_error(self):
        with self.assertRaises(ValueError):
            SecureSocket(host=None, port=8000)

    # --- Port validation ---
    def test_port_too_high_raises_value_error(self):
        with self.assertRaises(ValueError):
            SecureSocket(host='127.0.0.1', port=70000)

    def test_port_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            SecureSocket(host='127.0.0.1', port=0)

    def test_port_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            SecureSocket(host='127.0.0.1', port=-1)

    def test_port_non_integer_raises_value_error(self):
        with self.assertRaises(ValueError):
            SecureSocket(host='127.0.0.1', port='8000')

    def test_port_boundary_low(self):
        sock = SecureSocket(host='127.0.0.1', port=1)
        self.assertEqual(sock.port, 1)

    def test_port_boundary_high(self):
        sock = SecureSocket(host='127.0.0.1', port=65535)
        self.assertEqual(sock.port, 65535)


if __name__ == "__main__":
    unittest.main()
