from app.common.utils import unigram_frequencies
from app.common.types import TransformCase

def encrypt_text(original_text: str, key: int) -> str:
    encrypted_text = ""
    alphabet = sorted(unigram_frequencies().keys())

    for character in original_text:
        original_position = alphabet.index(character.lower()) if character.lower() in alphabet else None
        if original_position is None:
            encrypted_text = encrypted_text + character
        else:
            encrypted_position = (original_position + key) % 26
            encrypted_character = alphabet[encrypted_position]
            encrypted_text = encrypted_text + (encrypted_character.upper() if character.isupper() else encrypted_character)
    
    return encrypted_text

def transform_text(text: str, keep_spaces: bool, keep_punctation: bool, transform_case: TransformCase) -> str:
    if transform_case == TransformCase.LOWERCASE:
        text = text.lower()
    elif transform_case == TransformCase.UPPERCASE:
        text = text.upper()

    chars = []
    for char in text:
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
    
    transformed_text = ''.join(chars)
    return transformed_text
