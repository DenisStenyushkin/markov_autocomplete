"""Provides tools to tokenise texts"""

from nltk.tokenize import word_tokenize
import string

def tokenize(source):
    """Tokenises the provided source.
    Result will include only words, but not punctuation or digits

    Args:
        source (str): a string to tokenise

    Returns:
        list of str: a sequence of extracted tokens
    """
    all_tokens = word_tokenize(source)
    filtered_tokens = [t for t in all_tokens if t.isalpha()]
    return list(filtered_tokens)
