from .utils import load_json_file, count_alpha_characters
from .types import TransformCase
import os
from pprint import pprint

current_dir = os.path.dirname(os.path.abspath(__file__))

def encrypt_message(original_message: str, key: int):
    encrypted_message = ""
    json_path = os.path.join(current_dir, '..', 'data', 'letter_frequencies.json')
    alphabet = sorted(load_json_file(json_path).keys())

    for character in original_message:
        original_position = alphabet.index(character.lower()) if character.lower() in alphabet else None
        if original_position is None:
            encrypted_message = encrypted_message + character
        else:
            encrypted_position = (original_position + key) % 26
            encrypted_character = alphabet[encrypted_position]
            encrypted_message = encrypted_message + (encrypted_character.upper() if character.isupper() else encrypted_character)
    
    return encrypted_message

def transform_message(message: str, keep_spaces: bool, keep_punctation: bool, transform_case: TransformCase):
    if transform_case == TransformCase.LOWERCASE:
        message = message.lower()
    elif transform_case == TransformCase.UPPERCASE:
        message = message.upper()

    chars = []
    for char in message:
        if char == ' ':
            if keep_spaces:
                chars.append(char)
            # if not keep_spaces, skip the space
        elif not char.isalnum():
            if keep_punctation:
                chars.append(char)
            # if not keep_punctation, skip the punctuation
        else:
            chars.append(char)  # always keep alphanumeric chars
    
    transformed_message = ''.join(chars)
    return transformed_message

def standardised_frequencies(frequency_dictionary: dict, alpha_message_length: int):
    """ Standardising the chi-squared value for each letter / bigram to the alphabetical message length """
    for key, frequency in frequency_dictionary.items():
        frequency_dictionary[key] = round(frequency * alpha_message_length, 4)
    
    return frequency_dictionary

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