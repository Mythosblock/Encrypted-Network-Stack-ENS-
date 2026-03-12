import unittest
from src.encryption import SecureChannel


class TestEncryption(unittest.TestCase):
    def test_encrypt_decrypt(self):
        channel = SecureChannel()
        plaintext_message = b"test message"
        encrypted_token = channel.encrypt(plaintext_message)
        decrypted_message = channel.decrypt(encrypted_token)
        self.assertEqual(plaintext_message, decrypted_message)

    def test_key_generation(self):
        channel = SecureChannel()
        self.assertIsNotNone(channel.encryption_key)
        self.assertIsNotNone(channel.fernet_cipher)

    def test_different_channels_cannot_decrypt(self):
        sender_channel = SecureChannel()
        receiver_channel = SecureChannel()
        encrypted_token = sender_channel.encrypt(b"secret")
        with self.assertRaises(Exception):
            receiver_channel.decrypt(encrypted_token)


if __name__ == "__main__":
    unittest.main()
