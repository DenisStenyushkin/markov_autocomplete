"""Unit tests for tokeniser function"""
import unittest
from tokeniser import tokenize

class TokeniserTests(unittest.TestCase):
    """Test suit for tokenise function"""

    def test_simple_string(self):
        """Correctly tokenises a simple string"""
        s = "it is a simple string"
        tokens = tokenize(s)
        self.assertListEqual(tokens,
            ['it', 'is', 'a', 'simple', 'string'])
