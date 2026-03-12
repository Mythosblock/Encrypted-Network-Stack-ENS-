class SecureSocket:
    """Secure socket wrapper for network connections."""

    def __init__(self, host: str = '127.0.0.1', port: int = 8000):
        """Initialize a SecureSocket.

        Args:
            host: The host address to connect to.
            port: The port number (must be between 1 and 65535).

        Raises:
            ValueError: If host is empty or port is out of range.
        """
        if not isinstance(host, str) or not host:
            raise ValueError("Host must be a non-empty string")
        if not isinstance(port, int) or not (1 <= port <= 65535):
            raise ValueError("Port must be an integer between 1 and 65535")
        self.host = host
        self.port = port

    def connect(self):
        """Attempt to connect to the configured host and port."""
        print(f"Connecting to {self.host}:{self.port}")
