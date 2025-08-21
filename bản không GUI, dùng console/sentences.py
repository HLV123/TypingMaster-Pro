# sentences.py
import random

SENTENCE_LIST = [
    "The quick brown fox jumps over the lazy dog.",
    "Python is a high-level, interpreted, general-purpose programming language.",
    "Never underestimate the power of a good book.",
    "The sun always shines brightest after the rain.",
    "Technology has revolutionized the way we live and work."
]

def get_random_sentence():
    """Returns a random sentence from the list."""
    return random.choice(SENTENCE_LIST)