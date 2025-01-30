from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from http import HTTPStatus
from app.core.types import EncryptionRequest, ApiResponse, ErrorDetail, ApiSolution
from app.core.utils import normalize_key
from app.core.errors import InvalidKeyError, error_logger
from app.core.encryption import encrypt_text, transform_text
from app.core.cracking import crack_cipher
import uuid

bp = Blueprint('decrypt', __name__)

@bp.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        data = EncryptionRequest(**request.get_json())
        if data.key is None:
            # if key not provided, hack the ciphertext
            hack_result = crack_cipher(data.text)
            transformed_solutions: list[ApiSolution] = [{
                'key': s.key, 
                'text': transform_text(s.full_text, data.keep_spaces, data.keep_punctuation, data.transform_case),
                'chi_squared_total': s.chi_squared_total
            } for s in hack_result.solutions]

            response = ApiResponse(
                success=True,
                data=transformed_solutions,
                metadata={
                    'confidence_level': hack_result.confidence_level,
                    'analysis_length': hack_result.analysis_length
                }
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
                    'text': transformed_text
                }],
                metadata={
                    'key': normalized_key
                }
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
        error_id = str(uuid.uuid4())
        error_logger(error, error_id)

        response = ApiResponse(
            success=False,
            error=ErrorDetail(
                code="INTERNAL_ERROR",
                message="An unexpected error occurred",
                error_id=error_id
            )
        )
        return jsonify(response.model_dump()), HTTPStatus.INTERNAL_SERVER_ERROR