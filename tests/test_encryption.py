import unittest
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

    # ------------------------------------------------------------------
    # Optional key parameter — avoids unnecessary key generation
    # ------------------------------------------------------------------

    def test_init_with_existing_key(self):
        key = Fernet.generate_key()
        ch = SecureChannel(key=key)
        self.assertEqual(ch.key, key)
        # Must be able to round-trip with the supplied key
        token = ch.encrypt(b"hello")
        self.assertEqual(ch.decrypt(token), b"hello")

    def test_init_with_bytearray_key(self):
        key = bytearray(Fernet.generate_key())
        ch = SecureChannel(key=key)
        self.assertEqual(ch.key, bytes(key))

    def test_init_bad_key_type_raises(self):
        with self.assertRaises(TypeError):
            SecureChannel(key="not-bytes")

    # ------------------------------------------------------------------
    # Input validation
    # ------------------------------------------------------------------

    def test_encrypt_bad_type_raises(self):
        ch = SecureChannel()
        with self.assertRaises(TypeError):
            ch.encrypt("not bytes")

    def test_decrypt_bad_type_raises(self):
        ch = SecureChannel()
        with self.assertRaises(TypeError):
            ch.decrypt("not bytes")

    def test_decrypt_invalid_token_raises_value_error(self):
        ch = SecureChannel()
        with self.assertRaises(ValueError):
            ch.decrypt(b"invalid-token")

    # ------------------------------------------------------------------
    # Batch operations
    # ------------------------------------------------------------------

    def test_encrypt_batch(self):
        ch = SecureChannel()
        messages = [b"msg1", b"msg2", b"msg3"]
        tokens = ch.encrypt_batch(messages)
        self.assertEqual(len(tokens), len(messages))
        for original, token in zip(messages, tokens):
            self.assertEqual(ch.decrypt(token), original)

    def test_decrypt_batch(self):
        ch = SecureChannel()
        messages = [b"alpha", b"beta", b"gamma"]
        tokens = ch.encrypt_batch(messages)
        decrypted = ch.decrypt_batch(tokens)
        self.assertEqual(decrypted, messages)

    def test_decrypt_batch_invalid_token_raises_value_error(self):
        ch = SecureChannel()
        with self.assertRaises(ValueError):
            ch.decrypt_batch([b"bad-token"])

    def test_encrypt_batch_bytearray_input(self):
        ch = SecureChannel()
        messages = [bytearray(b"msg")]
        tokens = ch.encrypt_batch(messages)
        self.assertEqual(ch.decrypt(tokens[0]), b"msg")

    def test_decrypt_batch_bytearray_tokens(self):
        ch = SecureChannel()
        token = ch.encrypt(b"data")
        result = ch.decrypt_batch([bytearray(token)])
        self.assertEqual(result, [b"data"])

    def test_encrypt_batch_bad_container_raises(self):
        ch = SecureChannel()
        with self.assertRaises(TypeError):
            ch.encrypt_batch(b"not a list")

    def test_encrypt_batch_bad_element_raises(self):
        ch = SecureChannel()
        with self.assertRaises(TypeError):
            ch.encrypt_batch(["not bytes"])

    def test_decrypt_batch_bad_container_raises(self):
        ch = SecureChannel()
        with self.assertRaises(TypeError):
            ch.decrypt_batch(b"not a list")

    def test_decrypt_batch_bad_element_raises(self):
        ch = SecureChannel()
        with self.assertRaises(TypeError):
            ch.decrypt_batch(["not bytes"])

    def test_decrypt_ttl_valid(self):
        ch = SecureChannel()
        token = ch.encrypt(b"fresh")
        # Token was just created — a generous TTL must succeed
        result = ch.decrypt(token, ttl=60)
        self.assertEqual(result, b"fresh")

    def test_decrypt_ttl_expired_raises(self):
        import time
        ch = SecureChannel()
        token = ch.encrypt(b"stale")
        time.sleep(1)
        with self.assertRaises(ValueError):
            ch.decrypt(token, ttl=0)

    def test_decrypt_batch_ttl_valid(self):
        ch = SecureChannel()
        tokens = ch.encrypt_batch([b"a", b"b"])
        result = ch.decrypt_batch(tokens, ttl=60)
        self.assertEqual(result, [b"a", b"b"])


if __name__ == "__main__":
    unittest.main()
