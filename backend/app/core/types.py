from pydantic import BaseModel, Field
from typing import Optional, Dict
from enum import Enum

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

class EncryptionRequest(BaseModel):
    message: str = Field(..., max_length=5000, description="Message to be encrypted / decrypted")
    key: Optional[int] = Field(None, description="Shift key for encryption / decryption")
    keep_spaces: Optional[bool] = Field(default=True, description='')
    keep_punctuation: Optional[bool] = Field(default=True, description='')
    transform_case: TransformCase = Field(default=TransformCase.KEEP_CASE, description='')