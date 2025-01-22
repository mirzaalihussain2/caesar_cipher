from .utils import load_json_file
from .encryption import encrypt_message
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
from typing import TypedDict

letter_json_path = os.path.join(current_dir, '..', 'data', 'letter_frequencies.json')
bigram_json_path = os.path.join(current_dir, '..', 'data', 'bigram_frequencies.json')
normalised_expected_frequencies: dict = load_json_file(letter_json_path)
english_bigram_freq: dict = load_json_file(bigram_json_path)

class SolutionText(TypedDict):
    key: int
    text: str

class ScoredSolutionText(SolutionText):
    chi_squared_stat: float

def crack_cypher(ciphertext: str):
    solutions = generate_all_solutions(ciphertext)
    scored_solutions: list[ScoredSolutionText] = []

    # for each solution
        # clean text
        # get ngrams
        # get observed frequencies
        # calculate chi-sq stat
        # add to solution dictionary
    for solution in solutions:
        cleaned_text = clean_text(solution['text'])
        ngram_list = get_ngrams(cleaned_text, 1)
        observed_frequencies = get_observed_frequencies(ngram_list)
        chi_squared_stat = calculate_chi_squared_stat(observed_frequencies, normalised_expected_frequencies)
        scored_solutions.append({
            'key': solution['key'],
            'text': solution['text'],
            'chi_squared_stat': chi_squared_stat
        })

    print(scored_solutions)
    return scored_solutions


def generate_all_solutions(ciphertext: str) -> list[SolutionText]:
    solutions = []

    for key in range(26):
        solution = {
            'key': key,
            'text': encrypt_message(ciphertext, key)
        }
        solutions.append(solution)

    return solutions

def clean_text(text: str) -> str:
    return ''.join(character.lower() for character in text if character.isalpha() or character.isspace())

def get_ngrams(cleaned_text: str, n: int) -> list[str]:
    words = cleaned_text.split()
    
    ngrams = []
    for word in words:
        if len(word) >= n:
            word_ngrams = [word[i:i+n] for i in range(len(word)-n+1)]
            ngrams.extend(word_ngrams)
    
    return ngrams

# all elements in ngram_list should be alphabetic & lowercase 
def get_observed_frequencies(ngram_list: list[str]) -> dict[str, int]:
    observed_frequencies = {}
    for ngram in ngram_list:
        observed_frequencies[ngram] = observed_frequencies.get(ngram, 0) + 1
    
    return observed_frequencies

def calculate_chi_squared_stat(
    observed_frequencies: dict[str, int],
    normalised_expected_frequencies: dict[str, float]
) -> float:
    text_length = sum(observed_frequencies.values())
    chi_squared_stat = 0

    for character, normalised_expected_freq in normalised_expected_frequencies.items():
        observed_freq = observed_frequencies.get(character, 0)
        expected_freq = normalised_expected_freq * text_length
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