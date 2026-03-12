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
        with self.assertRaises(Exception):
            ch2.decrypt(token)

    # --- performance improvements ---

    def test_key_injection_reuses_provided_key(self):
        """Constructing a SecureChannel with an existing key must not generate
        a new one, allowing callers to skip the OS-entropy read."""
        ch1 = SecureChannel()
        ch2 = SecureChannel(key=ch1.key)
        self.assertEqual(ch1.key, ch2.key)
        # Channels with the same key must be able to decrypt each other's tokens.
        token = ch1.encrypt(b"shared key test")
        self.assertEqual(ch2.decrypt(token), b"shared key test")

    def test_encrypt_batch(self):
        channel = SecureChannel()
        messages = [b"msg1", b"msg2", b"msg3"]
        tokens = channel.encrypt_batch(messages)
        self.assertEqual(len(tokens), len(messages))
        for original, token in zip(messages, tokens):
            self.assertEqual(channel.decrypt(token), original)

    def test_decrypt_batch(self):
        channel = SecureChannel()
        messages = [b"alpha", b"beta", b"gamma"]
        tokens = channel.encrypt_batch(messages)
        decrypted = channel.decrypt_batch(tokens)
        self.assertEqual(decrypted, messages)

    def test_batch_roundtrip_empty(self):
        channel = SecureChannel()
        self.assertEqual(channel.encrypt_batch([]), [])
        self.assertEqual(channel.decrypt_batch([]), [])


if __name__ == "__main__":
    unittest.main()
