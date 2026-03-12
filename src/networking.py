import socket


class SecureSocket:
    """Thin TCP wrapper with lazy socket creation.

    The underlying ``socket.socket`` object is not allocated until
    ``connect()`` is called, avoiding OS-level resource allocation for
    nodes that are constructed but never actually connected.
    """

    def __init__(self, host: str = '127.0.0.1', port: int = 8000):
        self.host = host
        self.port = port
        self._sock: socket.socket | None = None

    def connect(self) -> None:
        """Open a TCP connection to ``host:port`` (lazy initialisation)."""
        if self._sock is None:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((self.host, self.port))

    def close(self) -> None:
        """Close the underlying socket if it has been opened."""
        if self._sock is not None:
            self._sock.close()
            self._sock = None
