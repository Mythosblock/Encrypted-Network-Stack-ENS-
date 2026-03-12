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

    # --- performance improvements ---

    def test_lazy_socket_not_created_on_init(self):
        """The underlying socket object must NOT be allocated at construction
        time; it should only exist after ``connect()`` is called."""
        sock = SecureSocket()
        self.assertIsNone(sock._sock)

    def test_close_before_connect_is_safe(self):
        """Calling ``close()`` on an unconnected socket must not raise."""
        sock = SecureSocket()
        sock.close()  # must not raise
        self.assertIsNone(sock._sock)

    def test_close_resets_sock(self):
        """After ``close()``, the internal socket reference must be cleared
        so a subsequent ``connect()`` allocates a fresh socket."""
        import socket as _socket

        sock = SecureSocket()
        # Manually set _sock to a real socket object to simulate post-connect.
        raw = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
        sock._sock = raw
        sock.close()
        self.assertIsNone(sock._sock)


if __name__ == "__main__":
    unittest.main()
