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

    def test_socket_invalid_host_raises(self):
        """Test that empty host is rejected."""
        with self.assertRaises(ValueError):
            SecureSocket(host='', port=8000)

    def test_socket_invalid_port_raises(self):
        """Test that port out of range is rejected."""
        with self.assertRaises(ValueError):
            SecureSocket(host='127.0.0.1', port=70000)

    def test_socket_port_zero_raises(self):
        """Test that port 0 is rejected."""
        with self.assertRaises(ValueError):
            SecureSocket(host='127.0.0.1', port=0)

    def test_socket_negative_port_raises(self):
        """Test that negative port is rejected."""
        with self.assertRaises(ValueError):
            SecureSocket(host='127.0.0.1', port=-1)

    def test_socket_non_int_port_raises(self):
        """Test that non-integer port is rejected."""
        with self.assertRaises(ValueError):
            SecureSocket(host='127.0.0.1', port="8000")  # type: ignore[arg-type]

    def test_socket_non_string_host_raises(self):
        """Test that non-string host is rejected."""
        with self.assertRaises(ValueError):
            SecureSocket(host=123, port=8000)  # type: ignore[arg-type]

    def test_socket_max_port(self):
        """Test that maximum valid port is accepted."""
        sock = SecureSocket(host='127.0.0.1', port=65535)
        self.assertEqual(sock.port, 65535)

    def test_socket_min_port(self):
        """Test that minimum valid port is accepted."""
        sock = SecureSocket(host='127.0.0.1', port=1)
        self.assertEqual(sock.port, 1)


if __name__ == "__main__":
    unittest.main()
