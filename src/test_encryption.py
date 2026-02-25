import unittest
from src.encryption import SecureChannel

class TestEncryption(unittest.TestCase):
    def test_encrypt_decrypt(self):
        channel = SecureChannel()
        msg = b"test"
        token = channel.encrypt(msg)
        self.assertEqual(channel.decrypt(token), msg)

if __name__ == "__main__":
    unittest.main()
