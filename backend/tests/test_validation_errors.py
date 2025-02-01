import pytest

test_cases = [
    {
        "description": "text is empty string",
        "text": ""
    },
    {
        "description": "text is whitespace only",
        "text": "   "
    },
    {
        "description": "text is exceeds max length",
        "text": "a" * 10001
    },
    {
        "description": "text is number",
        "text": 123
    },
    {
        "description": "text is boolean",
        "text": True
    },
    {
        "description": "text is list",
        "text": ["text"]
    },
    {
        "description": "text is dict",
        "text": {"text": "text"}
    },
    {
        "description": "key is float",
        "key": 5.5
    },
    {
        "description": "key is 0, INVALID_KEY error",
        "key": 0,
        "error_code": 'INVALID_KEY',
        "message": "Key cannot be 0. This won't encrypt your text.",
        "status_code": 422
    },
    {
        "description": "key is multiple of 26, INVALID_KEY error",
        "key": 104,
        "error_code": 'INVALID_KEY',
        "message": "Key cannot be a multiple of 26. This won't encrypt your text.",
        "status_code": 422
    },
    {
        "description": "invalid string for keep_spaces boolean",
        "keep_spaces": "hello"
    },
    {
        "description": "invalid integer for keep_punctuation boolean",
        "keep_punctuation": 34
    },
    {
        "description": "incorrect case for transform_case",
        "transform_case": "UPPERCASE"
    },
    {
        "description": "extra space for transform_case",
        "transform_case": "lowercase "
    },
    {
        "description": "transform_case is number",
        "transform_case": 1
    },
    {
        "description": "transform_case is boolean",
        "transform_case": True
    }
]

@pytest.mark.parametrize("test_params", test_cases)
def test_invalid_params(test_client, test_params):
    """ Test validation errors of all params: text, key, keep_spaces, keep_punctuation, transform_case """
    payload = {
        'text': test_params.get('text', 'Hello World'),
        **{param: test_params[param] for param in ['key', 'keep_spaces', 'keep_punctuation', 'transform_case'] 
        if param in test_params}
    }
    response = test_client.post('/encrypt', json=payload)
    assert response.status_code == test_params.get('status_code', 400)
    assert response.json['success'] == False
    assert response.json['error']['code'] == test_params.get('error_code', 'VALIDATION_ERROR')
    if test_params.get("message"):
        assert response.json['error']['message'] == test_params.get("message")

def test_missing_text_param(test_client):
    """ Test validation error when text parameter is missing """
    payload = {
        "key": 1
    }
    response = test_client.post('/encrypt', json=payload)
    assert response.status_code == 400
    assert response.json['success'] == False
    assert response.json['error']['code'] == 'VALIDATION_ERROR'