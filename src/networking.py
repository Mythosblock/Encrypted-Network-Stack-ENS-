class SecureSocket:
    def __init__(self, host='127.0.0.1', port=8000):
        if not isinstance(host, str) or not host:
            raise ValueError("host must be a non-empty string")
        if not isinstance(port, int) or not (1 <= port <= 65535):
            raise ValueError("port must be an integer in the range 1-65535")
        self.host = host
        self.port = port

    def connect(self):
        print(f"Connecting to {self.host}:{self.port}")
