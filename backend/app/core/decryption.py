from .utils import load_json_file, count_alpha_characters
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

def get_ngrams(text: str, n: int) -> list[str]:
    cleaned_text: str = ''.join(char.lower() for char in text if char.isalpha() or char.isspace())
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
    number_of_alphabetic_characters = count_alpha_characters(message)
    
    letter_json_path = os.path.join(current_dir, '..', 'data', 'letter_frequencies.json')
    bigram_json_path = os.path.join(current_dir, '..', 'data', 'bigram_frequencies.json')
    english_lang_freq: dict = load_json_file(letter_json_path)
    english_bigram_freq: dict = load_json_file(bigram_json_path)
    
    keys_table(english_lang_freq, english_bigram_freq)