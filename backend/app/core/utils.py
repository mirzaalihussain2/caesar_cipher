from typing import Literal
import json
from .errors import InvalidKeyError
from .types import StatName, ConfidenceLevel, ConfidenceThreshold
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CURRENT_DIR, '..', 'data')
MIN_BIGRAM_TEXT_LENGTH = 200
DECIMAL_PLACES = 5
ANALYSIS_LENGTHS = [2000, 5000, 8000]

CONFIDENCE_THRESHOLDS: dict[ConfidenceLevel, ConfidenceThreshold] = {
    ConfidenceLevel.LOW: ConfidenceThreshold(
        z_statistic=1.5,
        separation_score=1.0,
        relative_rank=0.5
    ),
    ConfidenceLevel.HIGH: ConfidenceThreshold(
        z_statistic=3.0,
        separation_score=2.0,
        relative_rank=0.2,
    )
}

def load_json_file(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def unigram_frequencies():
    filepath = os.path.join(DATA_DIR, 'letter_frequencies.json')
    return load_json_file(filepath)

def bigram_frequencies():
    filepath = os.path.join(DATA_DIR, 'bigram_frequencies.json')
    return load_json_file(filepath)

def get_ngram_weight(stat_name: StatName, text_length: int) -> float:
    weight_unigram = max(0.5, 1 - (0.0002*text_length))
    weight_bigram = 1 - weight_unigram

    return round(weight_unigram if stat_name == StatName.UNIGRAM else weight_bigram, DECIMAL_PLACES)

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

def get_ngrams(text: str, ngram_size: int) -> list[str]:
    cleaned_text = clean_text(text)
    words = cleaned_text.split()
    
    ngrams = []
    for word in words:
        if len(word) >= ngram_size:
            word_ngrams = [word[i:i+ngram_size] for i in range(len(word)-ngram_size+1)]
            ngrams.extend(word_ngrams)
    
    return ngrams

def get_observed_frequencies(text: str, ngram_size: int) -> dict[str, int]:
    observed_frequencies = {}
    ngrams = get_ngrams(text, ngram_size)

    for ngram in ngrams:
        observed_frequencies[ngram] = observed_frequencies.get(ngram, 0) + 1
    
    return observed_frequencies
