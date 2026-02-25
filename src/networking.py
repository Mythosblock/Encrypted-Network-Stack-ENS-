class SecureSocket:
    def __init__(self, host='127.0.0.1', port=8000):
        self.host = host
        self.port = port

    def connect(self):
        print(f"Connecting to {self.host}:{self.port}")
