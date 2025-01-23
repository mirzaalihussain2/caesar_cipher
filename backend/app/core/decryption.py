from .utils import load_json_file, count_alpha_characters
from .encryption import encrypt_message
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
from typing import TypedDict
from pprint import pprint

letter_json_path = os.path.join(current_dir, '..', 'data', 'letter_frequencies.json')
bigram_json_path = os.path.join(current_dir, '..', 'data', 'bigram_frequencies.json')
normalised_expected_frequencies: dict = load_json_file(letter_json_path)
english_bigram_freq: dict = load_json_file(bigram_json_path)

class SolutionText(TypedDict):
    key: int
    text: str
    chi_squared_stats: dict[str, float]
    chi_squared_total: float | None

class ScoredSolutionText(SolutionText):
    chi_squared_stat: float


# only use bigrams if ciphertext > 50 characters
# otherwise only use letters / unigrams
# doesn't make sense to do bigram compute if <50 characters

def hacky_boi(
        solutions: list[SolutionText],
        ngram_size: int,
        normalised_expected_frequencies: dict[str, float],
        stat_name: str
) -> list[SolutionText]:
    for solution in solutions:
        chi_squared_stat = calculate_chi_squared_stat(
            text=solution['text'],
            ngram_size=ngram_size,
            normalised_expected_frequencies=normalised_expected_frequencies
        )
        solution['chi_squared_stats'][stat_name] = chi_squared_stat
    
    return solutions

# maybe rename NORMALISED_EXPECTED_FREQUENCIES to NGRAM_EXPECTED_FREQUENCIES
# because they pertain to specific NGRAMS (e.g. unigrams, bigrams, trigrams)
def crack_cypher(ciphertext: str):

    text_length = count_alpha_characters(ciphertext)

    solutions = hacky_boi(
        solutions=generate_all_solutions(ciphertext),
        ngram_size=1,
        normalised_expected_frequencies=normalised_expected_frequencies,
        stat_name='unigrams'
    )

    pprint(solutions)
    return solutions

def generate_all_solutions(ciphertext: str) -> list[SolutionText]:
    solutions = []

    for key in range(26):
        solution = {
            'key': key,
            'text': encrypt_message(ciphertext, key),
            'chi_squared_stats': {},
            'chi_squared_total': None
        }
        solutions.append(solution)

    return solutions

def clean_text(text: str) -> str:
    return ''.join(character.lower() for character in text if character.isalpha() or character.isspace())

def get_ngrams(text: str, ngram_size: int) -> list[str]:
    cleaned_text = clean_text(text)
    words = cleaned_text.split()
    
    ngrams = []
    for word in words:
        if len(word) >= ngram_size:
            word_ngrams = [word[i:i+ngram_size] for i in range(len(word)-ngram_size+1)]
            ngrams.extend(word_ngrams)
    
    return ngrams

# all elements in ngram_list should be alphabetic & lowercase 
def get_observed_frequencies(text: str, ngram_size: int) -> dict[str, int]:
    observed_frequencies = {}
    ngrams = get_ngrams(text, ngram_size)

    for ngram in ngrams:
        observed_frequencies[ngram] = observed_frequencies.get(ngram, 0) + 1
    
    return observed_frequencies

def calculate_chi_squared_stat(
    text: str,
    ngram_size: int,
    normalised_expected_frequencies: dict[str, float]
) -> float:
    observed_frequencies = get_observed_frequencies(text, ngram_size)
    text_length = sum(observed_frequencies.values())
    chi_squared_stat = 0
    expected_frequencies = {k: v * text_length for k, v in normalised_expected_frequencies.items()}

    for ngram, expected_freq in expected_frequencies.items():
        observed_freq = observed_frequencies.get(ngram, 0)
        chi_squared_stat += ((observed_freq - expected_freq) ** 2) / expected_freq if expected_freq != 0 else 0
    
    return chi_squared_stat



# old functions
def keys_table(letter_frequency_dictionary: dict, bigram_frequency_dictionary: dict):
    letter_dict = {key: 0 for key in letter_frequency_dictionary.keys()}
    bigram_dict = {key: 0 for key in bigram_frequency_dictionary.keys()}

    keys_dict = dict()
    for i in range(0, 26):
        keys_dict[i] = ["", 0, letter_dict, letter_dict, 0, bigram_dict, bigram_dict, 0]
    
    for i in range(5):
        print(f"Key {i}: {keys_dict[i]}")
    return keys_dict

def hack_cypher(message: str):    
    letter_json_path = os.path.join(current_dir, '..', 'data', 'letter_frequencies.json')
    bigram_json_path = os.path.join(current_dir, '..', 'data', 'bigram_frequencies.json')
    english_lang_freq: dict = load_json_file(letter_json_path)
    english_bigram_freq: dict = load_json_file(bigram_json_path)
    
    keys_table(english_lang_freq, english_bigram_freq)