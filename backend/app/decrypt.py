from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from http import HTTPStatus
import inspect
import logging
from app.core.types import EncryptionRequest, ApiResponse, ErrorDetail
from app.core.utils import normalize_key, count_alphabetic_characters
from app.core.errors import InvalidKeyError
from app.core.encryption import encrypt_message, transform_message

bp = Blueprint('decrypt', __name__)

@bp.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        data = EncryptionRequest(**request.get_json())
        if data.key is None:
            
            # get number of alphabetic character in encrypted message, for frequency analysis
            number_of_alphabetic_characters = count_alphabetic_characters(data.message)            

            response = ApiResponse(
                success=True,
                data="hacked message"
            )
            return jsonify(response.model_dump()), HTTPStatus.OK
        else:
            key = -(data.key)
            normalized_key = normalize_key(key, 'decrypt')
            decrypted_message = encrypt_message(data.message, normalized_key)
            transformed_message = transform_message(decrypted_message, data.keep_spaces, data.keep_punctuation, data.transform_case)
            
            response = ApiResponse(
                success=True,
                data=transformed_message,
                metadata={'key':normalized_key}
            )
            return jsonify(response.model_dump()), HTTPStatus.OK

        # if key provided
        # normalise key - raising error if key = 0 (i.e. message already decrpyted)
        # or, if key = 0, then hack as usual
        # or, if key = 0, return message to user & let them know that if they want to hack the message, then can
    
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