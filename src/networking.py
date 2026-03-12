class SecureSocket:
    def __init__(self, host='127.0.0.1', port=8000):
        if not isinstance(host, str) or not host:
            raise ValueError("Host must be a non-empty string")
        if not isinstance(port, int) or not (1 <= port <= 65535):
            raise ValueError("Port must be an integer between 1 and 65535")
        self.host = host
        self.port = port

    def connect(self):
        print(f"Connecting to {self.host}:{self.port}")
