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

class ApiResponse(BaseModel):
    success: bool
    data: Optional[list[dict]] = None
    error: Optional[ErrorDetail] = None
    metadata: Optional[dict] = None

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

class ApiSolution(SolutionWithTotal):
    """ Solution formatted for API responses. """
    model_config = ConfigDict(json_schema_extra={"exclude": ["chi_squared_stats", "normalised_chi_squared_stats"]})

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
    keep_spaces: Optional[bool] = Field(default=True, description='')
    keep_punctuation: Optional[bool] = Field(default=True, description='')
    transform_case: TransformCase = Field(default=TransformCase.KEEP_CASE, description='')

    @field_validator('text')
    @classmethod
    def validate_non_empty_text(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Text cannot be empty")
        return v