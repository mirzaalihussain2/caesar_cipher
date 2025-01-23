from .utils import unigram_frequencies
from .types import TransformCase

def encrypt_message(original_message: str, key: int):
    encrypted_message = ""
    alphabet = sorted(unigram_frequencies().keys())

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
