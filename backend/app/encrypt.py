from pydantic import ValidationError
from flask import Blueprint, jsonify, request
import random
from http import HTTPStatus
import logging
import inspect
from app.common.types import ApiText, Metadata, EncryptionRequest, ApiResponse, ErrorDetail, Action
from app.common.utils import normalize_key
from app.common.errors import InvalidKeyError
from app.encryption.encrypt_cipher import encrypt_text, transform_text

bp = Blueprint('encrypt', __name__)

@bp.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        data = EncryptionRequest(**request.get_json())
        normalized_key = random.randint(1, 25) if data.key is None else normalize_key(data.key, 'encrypt')

        encrypted_text = encrypt_text(data.text, normalized_key)
        transformed_text = transform_text(encrypted_text, data.keep_spaces, data.keep_punctuation, data.transform_case)

        response = ApiResponse(
            success=True,
            data=[ApiText(
                text=transformed_text
            )],
            metadata=Metadata(
                action=Action.ENCRYPT,
                key=normalized_key
            )
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