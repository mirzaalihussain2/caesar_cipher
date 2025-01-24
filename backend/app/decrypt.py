from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from http import HTTPStatus
import inspect
import logging
from app.core.types import EncryptionRequest, ApiResponse, ErrorDetail, ApiSolution
from app.core.utils import normalize_key
from app.core.errors import InvalidKeyError
from app.core.encryption import encrypt_text, transform_text
from app.core.hacking import hack_cipher

bp = Blueprint('decrypt', __name__)

@bp.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        data = EncryptionRequest(**request.get_json())
        if data.key is None:
            # if key not provided, hack the ciphertext
            solutions: list[ApiSolution] = [{'key': s['key'], 'text': s['text'], 'chi_squared_total': s['chi_squared_total']} for s in hack_cipher(data.text)]
            transformed_solutions: list[ApiSolution] = [{'key': s['key'], 'text': transform_text(s['text'], data.keep_spaces, data.keep_punctuation, data.transform_case), 'chi_squared_total': s['chi_squared_total']} for s in solutions]

            response = ApiResponse(
                success=True,
                data=transformed_solutions
            )
            return jsonify(response.model_dump()), HTTPStatus.OK
        else:
            # if provided, decrypt ciphertext with key
            key = -(data.key)
            normalized_key = normalize_key(key, 'decrypt')
            decrypted_text = encrypt_text(data.text, normalized_key)
            transformed_text = transform_text(decrypted_text, data.keep_spaces, data.keep_punctuation, data.transform_case)
            
            response = ApiResponse(
                success=True,
                data=[{
                    'text': transformed_text,
                    'key': normalized_key
                }]
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