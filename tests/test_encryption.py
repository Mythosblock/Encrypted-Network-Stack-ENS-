import unittest
from src.encryption import SecureChannel


class TestEncryption(unittest.TestCase):
    def test_encrypt_decrypt(self):
        channel = SecureChannel()
        msg = b"test message"
        token = channel.encrypt(msg)
        decrypted = channel.decrypt(token)
        self.assertEqual(msg, decrypted)

    def test_key_generation(self):
        channel = SecureChannel()
        self.assertIsNotNone(channel.key)
        self.assertIsNotNone(channel.cipher)

    def test_different_channels_cannot_decrypt(self):
        ch1 = SecureChannel()
        ch2 = SecureChannel()
        token = ch1.encrypt(b"secret")
        with self.assertRaises(ValueError):
            ch2.decrypt(token)

    def test_encrypt_requires_bytes(self):
        channel = SecureChannel()
        with self.assertRaises(TypeError):
            channel.encrypt("not-bytes")  # type: ignore[arg-type]

    def test_decrypt_rejects_invalid_token(self):
        channel = SecureChannel()
        with self.assertRaises(ValueError):
            channel.decrypt(b"not-a-valid-token")

    def test_decrypt_requires_bytes(self):
        channel = SecureChannel()
        with self.assertRaises(TypeError):
            channel.decrypt("string-token")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
