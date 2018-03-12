"""Unit tests for MarkovAutocompleteProvider class"""

import unittest
from MarkovAutocompleteProvider import MarkovAutocompleteProvider

class MarkovAutocompleteProvider_update_tests(unittest.TestCase):
    """Test suite for update method"""

    def test_adds_base_word(self):
        """update method correctly adds new base word (and consequent word)"""
        provider = MarkovAutocompleteProvider()
        provider.update("one", "fish")
        self.assertEqual(provider.distribution["one"]["fish"], 1)

    def test_adds_consequent_word(self):
        """update correctly adds new consequent word to an existing base word"""
        provider = MarkovAutocompleteProvider()
        provider.update("fish", "two")
        provider.update("fish", "red")

        self.assertEqual(provider.distribution["fish"]["two"], 1)
        self.assertEqual(provider.distribution["fish"]["red"], 1)

    def test_updates_consequent_word(self):
        """update correctly updates existing consequent word"""
        provider = MarkovAutocompleteProvider()
        provider.update("fish", "two")
        provider.update("fish", "red")
        provider.update("fish", "red")

        self.assertEqual(provider.distribution["fish"]["two"], 1)
        self.assertEqual(provider.distribution["fish"]["red"], 2)

class MarkovAutocompleteProvider_provide_tests(unittest.TestCase):
    """Test suite for provide method"""

    def setUp(self):
        self.provider = MarkovAutocompleteProvider()
        self.provider.distribution = {"fish": {"raw": 1, "read": 3, "red": 6, "foo": 1}}

    def test_provides_for_prefix_and_freq(self):
        suggestions = self.provider.provide("fish", "r", 0.25)
        self.assertTupleEqual(suggestions, ("red", "read"))

    def test_provides_for_prefix(self):
        suggestions = self.provider.provide("fish", "r")
        self.assertTupleEqual(suggestions, ("red", "read", "raw"))

    def test_provides_for_min_freq(self):
        suggestions = self.provider.provide("fish", min_freq=0.5)
        self.assertTupleEqual(suggestions, ("red",))

    def test_provides_for_base_word_only(self):
        suggestions = self.provider.provide("fish")
        self.assertTupleEqual(suggestions, ("red", "read", "raw", "foo"))
