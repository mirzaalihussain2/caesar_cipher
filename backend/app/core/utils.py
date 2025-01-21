from typing import Literal
import json
from .errors import InvalidKeyError

def normalize_key(key: int, encrypt_or_decrypt: Literal['encrypt', 'decrypt'] = 'encrypt') -> int:
    if key == 0:
        raise InvalidKeyError(f"Key cannot be 0. This won't {encrypt_or_decrypt} your message.")

    normalized_key = key % 26
    if normalized_key == 0:
        raise InvalidKeyError(f"Key cannot be a multiple of 26. This won't {encrypt_or_decrypt} your message.")

    return normalized_key

def load_json_file(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def count_alphabetic_characters(message: str) -> int:
    return sum(1 for char in message if char.isalpha())