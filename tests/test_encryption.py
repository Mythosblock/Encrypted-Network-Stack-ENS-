import time
import unittest
from unittest import mock

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

    def test_rejects_non_bytes_message(self):
        channel = SecureChannel()
        with self.assertRaisesRegex(TypeError, "msg must be bytes or bytearray"):
            channel.encrypt("not-bytes")  # type: ignore[arg-type]

    def test_rejects_non_bytes_token(self):
        channel = SecureChannel()
        token = channel.encrypt(b"ok")
        with self.assertRaisesRegex(TypeError, "token must be bytes or bytearray"):
            channel.decrypt("not-bytes")  # type: ignore[arg-type]
        # ensure decrypt still works for valid token
        self.assertEqual(channel.decrypt(token), b"ok")

    def test_token_expires(self):
        channel = SecureChannel(ttl=1)
        base_time = 1_000_000_000  # deterministic base timestamp
        with mock.patch("time.time", return_value=base_time), mock.patch(
            "cryptography.fernet.time.time", return_value=base_time
        ):
            token = channel.encrypt(b"ephemeral")
            self.assertEqual(channel.decrypt(token), b"ephemeral")
        with mock.patch(
            "time.time", return_value=base_time + 2
        ), mock.patch(
            "cryptography.fernet.time.time",
            return_value=base_time + 2,
        ):
            with self.assertRaises(ValueError):
                channel.decrypt(token)

    def test_rejects_tampered_token(self):
        channel = SecureChannel()
        with self.assertRaises(ValueError):
            channel.decrypt(b"not-a-valid-token")

    def test_invalid_ttl_rejected(self):
        with self.assertRaises(ValueError):
            SecureChannel(ttl=0)

    def test_non_numeric_ttl_rejected(self):
        with self.assertRaises(TypeError):
            SecureChannel(ttl="not-a-number")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
