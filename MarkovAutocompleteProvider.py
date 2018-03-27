"""
Provides MarkovAutocompleteProvider class
that utilises Markov model to provide autocomplete suggestions
"""

import pickle

class MarkovAutocompleteProvider(object):
    MODEL_FILE_NAME = "model.dat"

    """
    Word autocomplete provider based on first-order Markov model
    """
    def __init__(self):
        # Word count distribution
        # Keys: base (previously typed by a user) words
        # Values: cont distribution
        # over consequent words (autocomplete suggestions) as a dict
        # The dict Keys: consequent word
        # The dict Values: the word's count
        self.distribution = {}

    def update(self, base_word, consequent_word):
        """Updates the provider's Markov model with a new word

        Args:
            base_word (str): a base word to be updated
            consequent_word (str): a consequent word to be updated
        """
        if base_word in self.distribution:
            if consequent_word in self.distribution[base_word]:
                self.distribution[base_word][consequent_word] += 1
            else:
                self.distribution[base_word][consequent_word] = 1
        else:
            self.distribution[base_word] = {}
            self.distribution[base_word][consequent_word] = 1

    def provide(self, base_word, prefix='', min_freq=0.0):
        """ Provides autocomplete suggestions according to specified parameters

        Args:
            base_word (str): a base word
            prefix (str, optional): suggestion prefix
            min_freq (float, optional): minimum suggestion frequency as fraction
                to be included

        Returns:
            tuple: suggestions sorted by frequency descending.
                An empty iterable will be returned if no suggestions found.
        """
        if base_word not in self.distribution:
            return ()

        counts = self.distribution[base_word]
        min_freq = min(min_freq, 1)
        total_count = sum(counts.values())
        min_count = round(min_freq * total_count)

        counts = {key: value for key, value in counts.items()
                  if key.startswith(prefix) and value >= min_count}
        suggestions = sorted(counts.items(), key=lambda i: i[1], reverse=True)

        return tuple(s[0] for s in suggestions)

    def fit(self, corpus, tokeniser):
        """ Fits the provider's Markov model to provided text corpus

        Args:
            corpus (iterable of str): text corpus to fit the provider to
            tokeniser (callable): a callable that performs tokenisation
                must accept a str parameter as a source string and return a list of str
                as a sequence of extracted tokens
        """
        for text in corpus:
            tokens = tokeniser(text)
            for i, _ in enumerate(tokens[:-1]):
                self.update(tokens[i], tokens[i+1])

    def save(self):
        """ Saves the provider's Markov model to disk """
        with open(self.MODEL_FILE_NAME, "wb") as f:
            pickle.dump(self.distribution, f)

    def load(self):
        """ Loads th provider's Markov model from disk """
        with open(self.MODEL_FILE_NAME, "rb") as f:
            self.distribution = pickle.load(f)
