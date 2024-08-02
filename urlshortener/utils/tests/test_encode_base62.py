from unittest import TestCase

from urlshortener.utils.encode_base62 import encode_base62


class TestBase62Encoding(TestCase):
    def test_encode_zero(self):
        self.assertEqual(encode_base62(0), "0")

    def test_encode_single_digit(self):
        self.assertEqual(encode_base62(1), "1")
        self.assertEqual(encode_base62(9), "9")

    def test_encode_single_letter(self):
        self.assertEqual(encode_base62(10), "a")
        self.assertEqual(encode_base62(35), "z")
        self.assertEqual(encode_base62(36), "A")
        self.assertEqual(encode_base62(61), "Z")

    def test_encode_multiple_digits(self):
        self.assertEqual(encode_base62(62), "10")
        self.assertEqual(encode_base62(3843), "ZZ")
        self.assertEqual(encode_base62(123456789), "8m0Kx")

    def test_encode_large_number(self):
        self.assertEqual(encode_base62(9876543210), "aMoY42")
