"""Unit tests for MarkovAutocompleteProvider class"""

import unittest
from MarkovAutocompleteProvider import MarkovAutocompleteProvider
from tokeniser import tokenize

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
        self.provider.distribution = {"red": {"fish": 3},
                                      "fish": {"raw": 1, "read": 3, "red": 6, "foo": 1}}

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

    def test_empty_for_unknown_base(self):
        suggestions = self.provider.provide("qwerty")
        self.assertTupleEqual(suggestions, ())

    def test_handles_huge_min_freq(self):
        suggestions = self.provider.provide("red", "f", 100)
        self.assertTupleEqual(suggestions, ("fish",))

    def test_empty_for_unknown_prefix(self):
        suggestions = self.provider.provide("fish", "a")
        self.assertTupleEqual(suggestions, ())

class MarkovAutocompleteProvider_fit_tests(unittest.TestCase):
    """Test suite for fit method"""

    def test_handles_corpus(self):
        provider = MarkovAutocompleteProvider()
        corpus = ["harry is a good boy", "london is interesting", "harry potter is a wizard"]
        provider.fit(corpus, tokenize)
        self.assertDictEqual(provider.distribution, {"harry": {"is": 1, "potter": 1},
                                                     "is": {"a": 2, "interesting": 1},
                                                     "a": {"good": 1, "wizard": 1},
                                                     "good": {"boy": 1},
                                                     "london": {"is": 1},
                                                     "potter": {"is": 1}})
