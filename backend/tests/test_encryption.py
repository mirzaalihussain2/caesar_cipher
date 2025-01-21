import pytest
from app.routes.encrypt import TransformCase

test_cases = [
    # key=5 permutations
    (5, True, True, TransformCase.LOWERCASE, "PLACEHOLDER"),
    (5, True, True, TransformCase.UPPERCASE, "PLACEHOLDER"),
    (5, True, True, TransformCase.KEEP_CASE, "PLACEHOLDER"),
    (5, True, False, TransformCase.LOWERCASE, "PLACEHOLDER"),
    (5, True, False, TransformCase.UPPERCASE, "PLACEHOLDER"),
    (5, True, False, TransformCase.KEEP_CASE, "PLACEHOLDER"),
    (5, False, True, TransformCase.LOWERCASE, "PLACEHOLDER"),
    (5, False, True, TransformCase.UPPERCASE, "PLACEHOLDER"),
    (5, False, True, TransformCase.KEEP_CASE, "PLACEHOLDER"),
    (5, False, False, TransformCase.LOWERCASE, "PLACEHOLDER"),
    (5, False, False, TransformCase.UPPERCASE, "PLACEHOLDER"),
    (5, False, False, TransformCase.KEEP_CASE, "PLACEHOLDER"),
    
    # key=13 permutations
    (13, True, True, TransformCase.LOWERCASE, "PLACEHOLDER"),
    (13, True, True, TransformCase.UPPERCASE, "PLACEHOLDER"),
    (13, True, True, TransformCase.KEEP_CASE, "PLACEHOLDER"),
    (13, True, False, TransformCase.LOWERCASE, "PLACEHOLDER"),
    (13, True, False, TransformCase.UPPERCASE, "PLACEHOLDER"),
    (13, True, False, TransformCase.KEEP_CASE, "PLACEHOLDER"),
    (13, False, True, TransformCase.LOWERCASE, "PLACEHOLDER"),
    (13, False, True, TransformCase.UPPERCASE, "PLACEHOLDER"),
    (13, False, True, TransformCase.KEEP_CASE, "PLACEHOLDER"),
    (13, False, False, TransformCase.LOWERCASE, "PLACEHOLDER"),
    (13, False, False, TransformCase.UPPERCASE, "PLACEHOLDER"),
    (13, False, False, TransformCase.KEEP_CASE, "PLACEHOLDER"),
    
    # key=18 permutations
    (18, True, True, TransformCase.LOWERCASE, "PLACEHOLDER"),
    (18, True, True, TransformCase.UPPERCASE, "PLACEHOLDER"),
    (18, True, True, TransformCase.KEEP_CASE, "PLACEHOLDER"),
    (18, True, False, TransformCase.LOWERCASE, "PLACEHOLDER"),
    (18, True, False, TransformCase.UPPERCASE, "PLACEHOLDER"),
    (18, True, False, TransformCase.KEEP_CASE, "PLACEHOLDER"),
    (18, False, True, TransformCase.LOWERCASE, "PLACEHOLDER"),
    (18, False, True, TransformCase.UPPERCASE, "PLACEHOLDER"),
    (18, False, True, TransformCase.KEEP_CASE, "PLACEHOLDER"),
    (18, False, False, TransformCase.LOWERCASE, "PLACEHOLDER"),
    (18, False, False, TransformCase.UPPERCASE, "PLACEHOLDER"),
    (18, False, False, TransformCase.KEEP_CASE, "PLACEHOLDER"),
    
    # key=24 permutations
    (24, True, True, TransformCase.LOWERCASE, "PLACEHOLDER"),
    (24, True, True, TransformCase.UPPERCASE, "PLACEHOLDER"),
    (24, True, True, TransformCase.KEEP_CASE, "PLACEHOLDER"),
    (24, True, False, TransformCase.LOWERCASE, "PLACEHOLDER"),
    (24, True, False, TransformCase.UPPERCASE, "PLACEHOLDER"),
    (24, True, False, TransformCase.KEEP_CASE, "PLACEHOLDER"),
    (24, False, True, TransformCase.LOWERCASE, "PLACEHOLDER"),
    (24, False, True, TransformCase.UPPERCASE, "PLACEHOLDER"),
    (24, False, True, TransformCase.KEEP_CASE, "PLACEHOLDER"),
    (24, False, False, TransformCase.LOWERCASE, "PLACEHOLDER"),
    (24, False, False, TransformCase.UPPERCASE, "PLACEHOLDER"),
    (24, False, False, TransformCase.KEEP_CASE, "PLACEHOLDER"),
]

@pytest.mark.parametrize("key,keep_spaces,keep_punctuation,transform_case,expected", test_cases)
def test_encryption_permutations(test_client, key, keep_spaces, keep_punctuation, transform_case, expected):
    """Test all permutations of encryption parameters"""
    payload = {
        "message": "Hello, World!",
        "key": key,
        "keep_spaces": keep_spaces,
        "keep_punctuation": keep_punctuation,
        "transform_case": transform_case.value
    }
    
    response = test_client.post('/encrypt', json=payload)
    assert response.status_code == 200
    assert response.json['success'] == True
    assert response.json['data'] == expected