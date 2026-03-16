import unittest
import time
from unittest.mock import patch
from cryptography.fernet import Fernet
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

    # --- Key validation ---
    def test_custom_valid_key(self):
        key = Fernet.generate_key()
        channel = SecureChannel(key=key)
        self.assertEqual(channel.key, key)

    def test_invalid_key_raises_value_error(self):
        with self.assertRaises(ValueError):
            SecureChannel(key=b"not-a-valid-fernet-key")

    def test_key_wrong_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            SecureChannel(key="stringkey")

    # --- TTL validation ---
    def test_ttl_wrong_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            SecureChannel(ttl="60")

    def test_ttl_float_accepted(self):
        channel = SecureChannel(ttl=1.5)
        self.assertEqual(channel.ttl, 1.5)

    # --- encrypt() type validation ---
    def test_encrypt_string_raises_type_error(self):
        channel = SecureChannel()
        with self.assertRaises(TypeError):
            channel.encrypt("not bytes")

    def test_encrypt_bytearray_accepted(self):
        channel = SecureChannel()
        token = channel.encrypt(bytearray(b"hello"))
        self.assertIsInstance(token, bytes)

    # --- decrypt() type validation ---
    def test_decrypt_string_raises_type_error(self):
        channel = SecureChannel()
        with self.assertRaises(TypeError):
            channel.decrypt("not bytes")

    def test_decrypt_invalid_token_raises_value_error(self):
        channel = SecureChannel()
        with self.assertRaises(ValueError):
            channel.decrypt(b"this-is-not-a-valid-fernet-token")

    def test_decrypt_tampered_token_raises_value_error(self):
        channel = SecureChannel()
        token = channel.encrypt(b"hello")
        tampered = bytearray(token)
        tampered[10] ^= 0xFF
        with self.assertRaises(ValueError):
            channel.decrypt(bytes(tampered))

    # --- TTL expiry ---
    def test_decrypt_expired_token_raises_value_error(self):
        channel = SecureChannel(ttl=1)
        token = channel.encrypt(b"hello")
        future_time = time.time() + 10
        with patch("time.time", return_value=future_time):
            with self.assertRaises(ValueError):
                channel.decrypt(token)

    # --- Batch operations ---
    def test_encrypt_batch_returns_list_of_tokens(self):
        channel = SecureChannel()
        msgs = [b"msg1", b"msg2", b"msg3"]
        tokens = channel.encrypt_batch(msgs)
        self.assertEqual(len(tokens), len(msgs))
        for token in tokens:
            self.assertIsInstance(token, bytes)

    def test_decrypt_batch_round_trips(self):
        channel = SecureChannel()
        msgs = [b"alpha", b"beta", b"gamma"]
        tokens = channel.encrypt_batch(msgs)
        decrypted = channel.decrypt_batch(tokens)
        self.assertEqual(decrypted, msgs)

    def test_encrypt_batch_empty(self):
        channel = SecureChannel()
        self.assertEqual(channel.encrypt_batch([]), [])

    def test_decrypt_batch_empty(self):
        channel = SecureChannel()
        self.assertEqual(channel.decrypt_batch([]), [])

    def test_encrypt_batch_type_error_propagates(self):
        channel = SecureChannel()
        with self.assertRaises(TypeError):
            channel.encrypt_batch([b"ok", "not bytes"])

    def test_decrypt_batch_invalid_token_propagates(self):
        channel = SecureChannel()
        with self.assertRaises(ValueError):
            channel.decrypt_batch([b"bad-token"])


if __name__ == "__main__":
    unittest.main()
