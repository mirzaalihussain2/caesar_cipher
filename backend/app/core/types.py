from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from typing import TypedDict

class ErrorDetail(BaseModel):
    code: str
    message: str

class ApiResponse(BaseModel):
    success: bool
    data: Optional[list[dict]] = None
    error: Optional[ErrorDetail] = None

class Solution(TypedDict):
    """
    Represents a possible solution when hacking a cipher.
    Lower chi_squared_total suggests better match to English language patterns.
    """
    key: int
    text: str
    chi_squared_stats: dict[str, float]
    chi_squared_total: float | None

class TransformCase(str, Enum):
    LOWERCASE = "lowercase"
    UPPERCASE = "uppercase"
    KEEP_CASE = "keep_case"

class EncryptionRequest(BaseModel):
    text: str = Field(..., max_length=5000, description="Text to be encrypted / decrypted")
    key: Optional[int] = Field(None, description="Shift key for encryption / decryption")
    keep_spaces: Optional[bool] = Field(default=True, description='')
    keep_punctuation: Optional[bool] = Field(default=True, description='')
    transform_case: TransformCase = Field(default=TransformCase.KEEP_CASE, description='')