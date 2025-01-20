from pydantic import BaseModel, Field, ValidationError
from typing import Optional
from flask import jsonify, request
from app.routes import bp
import random
import json
import os
from enum import Enum

class TransformCase(str, Enum):
    LOWERCASE = "lowercase"
    UPPERCASE = "uppercase"
    KEEP_CASE = "keep_case"

class InvalidKeyError(Exception):
    """ Raised when key is 0 or a multiple of 26 """
    pass

def normalized_key(key: Optional[int] = None) -> int:
    if key is None:
        return random.randint(1, 25)
    
    if key == 0:
        raise InvalidKeyError("Key cannot be 0. This won't encrypt your message.")

    normalized_key = key % 26
    if normalized_key == 0:
        raise InvalidKeyError("Key cannot be a multiple of 26. This won't encrypt your message.")

    return normalized_key

current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, '..', 'data', 'letter_frequencies.json')

def load_json_file(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)


def encrypt_message(original_message: str, key: int):
    encrypted_message = ""
    alphabet = sorted(load_json_file(json_path).keys())

    for character in original_message:
        original_position = alphabet.index(character) if character in alphabet else None
        if original_position is None:
            encrypted_message = encrypted_message + character
        else:
            encrypted_position = (original_position + key) % 26
            encrypted_message = encrypted_message + alphabet[encrypted_position]
    
    return encrypted_message

def transform_message(message: str, keepSpaces: bool, keepPunctation: bool, transformCase: TransformCase):
    if transformCase == TransformCase.LOWERCASE:
        message = message.lower()
    elif transformCase == TransformCase.UPPERCASE:
        message = message.upper()

    if not keepSpaces or not keepPunctation:
        chars = (char for char in message if (keepSpaces or char != ' ') and (keepPunctation or char.isalnum()))
        message = ''.join(chars)
    
    return message


class EncryptionRequest(BaseModel):
    message: str = Field(..., max_length=5000, description="Message to be encrypted / decrypted")
    key: Optional[int] = Field(None, description="Shift key for encryption / decryption")
    keep_spaces: Optional[bool] = Field(default=True, description='')
    keep_punctuation: Optional[bool] = Field(default=True, description='')
    transform_case: TransformCase = Field(default=TransformCase.KEEP_CASE, description='')


@bp.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        data = EncryptionRequest(**request.get_json())
        normalized_key = normalized_key(data.key)

        encrypted_message = encrypt_message(data.message, normalized_key)
        transformed_message = transform_message(encrypted_message, data.keepSpaces, data.keepPunctation, data.transformCase)

        return transformed_message

    except ValidationError:
        return 'error'
    except InvalidKeyError:
        return jsonify({
            InvalidKeyError
        })
    except Exception:
        return 'encrypted text'