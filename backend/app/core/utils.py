from typing import Literal
import json
from .errors import InvalidKeyError
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CURRENT_DIR, '..', 'data')

def load_json_file(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def unigram_frequencies():
    filepath = os.path.join(DATA_DIR, 'letter_frequencies.json')
    return load_json_file(filepath)

def bigram_frequencies():
    filepath = os.path.join(DATA_DIR, 'bigram_frequencies.json')
    return load_json_file(filepath)

def count_alpha_characters(text: str) -> int:
    return sum(1 for character in text if character.isalpha())

def clean_text(text: str) -> str:
    return ''.join(character.lower() for character in text if character.isalpha() or character.isspace())

def normalize_key(key: int, encrypt_or_decrypt: Literal['encrypt', 'decrypt'] = 'encrypt') -> int:
    if key == 0:
        raise InvalidKeyError(f"Key cannot be 0. This won't {encrypt_or_decrypt} your text.")

    normalized_key = key % 26
    if normalized_key == 0:
        raise InvalidKeyError(f"Key cannot be a multiple of 26. This won't {encrypt_or_decrypt} your text.")

    return normalized_key
