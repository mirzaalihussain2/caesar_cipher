from pydantic import BaseModel, Field, ValidationError
from typing import Optional, Dict
from flask import jsonify, request
from app.routes import bp
import random
import json
import os
from enum import Enum
from http import HTTPStatus
import logging
import inspect

class ErrorDetail(BaseModel):
    code: str
    message: str

class ApiResponse(BaseModel):
    success: bool
    data: Optional[str] = None
    metadata: Optional[Dict] = None
    error: Optional[ErrorDetail] = None

class TransformCase(str, Enum):
    LOWERCASE = "lowercase"
    UPPERCASE = "uppercase"
    KEEP_CASE = "keep_case"

class InvalidKeyError(Exception):
    """ Raised when key is 0 or a multiple of 26 """
    pass

def normalize_key(key: Optional[int] = None) -> int:
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

def transform_message(message: str, keep_spaces: bool, keep_punctation: bool, transform_case: TransformCase):
    if transform_case == TransformCase.LOWERCASE:
        message = message.lower()
    elif transform_case == TransformCase.UPPERCASE:
        message = message.upper()

    if not keep_spaces or not keep_punctation:
        chars = (char for char in message if (keep_spaces or char != ' ') and (keep_punctation or char.isalnum()))
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
        normalized_key = normalize_key(data.key)

        encrypted_message = encrypt_message(data.message, normalized_key)
        transformed_message = transform_message(encrypted_message, data.keep_spaces, data.keep_punctuation, data.transform_case)

        response = ApiResponse(
            success=True,
            data=transformed_message,
            metadata={'key':normalized_key}
        )
        return jsonify(response.model_dump()), HTTPStatus.OK

    except ValidationError as error:
        response = ApiResponse(
            success=False,
            error=ErrorDetail(
                code="VALIDATION_ERROR", 
                message=str(error)
            )
        )
        return jsonify(response.model_dump()), HTTPStatus.BAD_REQUEST
    
    except InvalidKeyError as error:
        response = ApiResponse(
            success=False,
            error=ErrorDetail(
                code="INVALID_KEY",
                message=str(error)
            )
        )
        return jsonify(response.model_dump()), HTTPStatus.UNPROCESSABLE_ENTITY
    
    except Exception as error:
        function_name = inspect.currentframe().f_code.co_name
        logging.error(f'Unexpected error in {function_name} function: {str(error)}')

        response = ApiResponse(
            success=False,
            error=ErrorDetail(
                code="INTERNAL_ERROR",
                message="An unexpected error occurred"

            )
        )
        return jsonify(response.model_dump()), HTTPStatus.INTERNAL_SERVER_ERROR