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

    def test_punctuation(self):
        """Correctly removes punctuation"""
        s = "it is a simple - but, look, still punctuated - string"
        tokens = tokenize(s)
        self.assertListEqual(tokens,
            ['it', 'is', 'a', 'simple', 'but', 'look', 'still', 'punctuated', 'string'])

    def test_extra_spaves(self):
        """Correctly tokenises a simple string"""
        s = "it is  a \t simple\n string"
        tokens = tokenize(s)
        self.assertListEqual(tokens,
            ['it', 'is', 'a', 'simple', 'string'])
