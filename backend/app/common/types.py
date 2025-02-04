from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from enum import Enum

class StatName(str, Enum):
    UNIGRAM = 'unigram'
    BIGRAM = 'bigram'
    # TRIGRAM = 'trigram'
    # QUADGRAM = 'quadgram'

class ConfidenceLevel(str, Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

class ConfidenceThreshold(BaseModel):
    z_statistic: float
    separation_score: float
    relative_rank: float

class ErrorDetail(BaseModel):
    code: str
    message: str
    error_id: Optional[str] = None

class Metadata(BaseModel):
    key: int
    confidence_level: Optional[ConfidenceLevel] = None
    analysis_length: Optional[int] = None

class Solution(BaseModel):
    """
    Represents a possible solution when hacking a cipher.
    Lower chi_squared_total suggests better match to English language patterns.
    """
    key: int
    full_text: str
    text: str
    chi_squared_stats: dict[StatName, float]
    normalised_chi_squared_stats: dict[StatName, float]

class SolutionWithTotal(Solution):
    """ Solution with calculated chi-squared total """
    chi_squared_total: float | None

class ApiSolution(BaseModel):
    """ Solution formatted for API responses. """
    key: int
    text: str
    chi_squared_total: float | None

class ApiText(BaseModel):
    text: str

class ApiResponse(BaseModel):
    success: bool
    data: Optional[list[ApiSolution | ApiText]] = None
    error: Optional[ErrorDetail] = None
    metadata: Optional[Metadata] = None

class TransformCase(str, Enum):
    LOWERCASE = "lowercase"
    UPPERCASE = "uppercase"
    KEEP_CASE = "keep_case"

class HackResult(BaseModel):
    solutions: list[SolutionWithTotal]
    confidence_level: ConfidenceLevel | None
    analysis_length: int | None

class EncryptionRequest(BaseModel):
    text: str = Field(..., max_length=10000, description="Text to be encrypted / decrypted")
    key: Optional[int] = Field(None, description="Shift key for encryption / decryption")
    keep_spaces: Optional[bool] = Field(default=True, description='Keep whitespace in return text')
    keep_punctuation: Optional[bool] = Field(default=True, description='Keep punctuation in return text')
    transform_case: TransformCase = Field(default=TransformCase.KEEP_CASE, description='Transform or maintain case in return text')

    @field_validator('text')
    @classmethod
    def validate_non_empty_text(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Text cannot be empty")
        return v