from __future__ import annotations

import socket


class SecureSocket:
    """Thin TCP wrapper with lazy socket initialisation.

    Performance notes
    -----------------
    * The underlying :class:`socket.socket` object is created only when
      :meth:`connect` is called (lazy init), so constructing many
      ``SecureSocket`` instances is cheap.
    * Host and port are validated eagerly in ``__init__`` so callers get
      fast, descriptive errors before any I/O happens.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 8000) -> None:
        if not isinstance(host, str) or not host:
            raise ValueError("host must be a non-empty string")
        if not isinstance(port, int) or not (1 <= port <= 65535):
            raise ValueError("port must be an integer in the range 1–65535")
        self.host = host
        self.port = port
        self._sock: socket.socket | None = None  # created lazily on connect()

    def connect(self) -> None:
        """Open a TCP connection to (host, port).

        The socket is created here rather than in ``__init__`` so that
        simply *describing* a connection carries no resource cost.
        """
        if self._sock is None:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((self.host, self.port))

    def close(self) -> None:
        """Close the underlying socket if it has been opened."""
        if self._sock is not None:
            self._sock.close()
            self._sock = None
