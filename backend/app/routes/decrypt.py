from app.routes import bp
from app.routes.encrypt import EncryptionRequest, ErrorDetail, ApiResponse, InvalidKeyError, normalize_key
from flask import jsonify, request
from pydantic import ValidationError
from http import HTTPStatus
import inspect
import logging

@bp.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        data = EncryptionRequest(**request.get_json())
        if data.key is None:
            # hack
            print("hack")
        else:
            normalized_key = normalize_key(data.key, 'decrypt')


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