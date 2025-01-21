import pytest
from app.routes.encrypt import TransformCase

# Base test case variations that will be applied to each encrypted message
base_variations = [
    dict(keep_spaces=True, keep_punctuation=True, transform_case=TransformCase.LOWERCASE, expected="hello, world!"),
    dict(keep_spaces=True, keep_punctuation=True, transform_case=TransformCase.UPPERCASE, expected="HELLO, WORLD!"),
    dict(keep_spaces=True, keep_punctuation=True, transform_case=TransformCase.KEEP_CASE, expected="Hello, World!"),
    dict(keep_spaces=True, keep_punctuation=False, transform_case=TransformCase.LOWERCASE, expected="hello world"),
    dict(keep_spaces=True, keep_punctuation=False, transform_case=TransformCase.UPPERCASE, expected="HELLO WORLD"),
    dict(keep_spaces=True, keep_punctuation=False, transform_case=TransformCase.KEEP_CASE, expected="Hello World"),
    dict(keep_spaces=False, keep_punctuation=True, transform_case=TransformCase.LOWERCASE, expected="hello,world!"),
    dict(keep_spaces=False, keep_punctuation=True, transform_case=TransformCase.UPPERCASE, expected="HELLO,WORLD!"),
    dict(keep_spaces=False, keep_punctuation=True, transform_case=TransformCase.KEEP_CASE, expected="Hello,World!"),
    dict(keep_spaces=False, keep_punctuation=False, transform_case=TransformCase.LOWERCASE, expected="helloworld"),
    dict(keep_spaces=False, keep_punctuation=False, transform_case=TransformCase.UPPERCASE, expected="HELLOWORLD"),
    dict(keep_spaces=False, keep_punctuation=False, transform_case=TransformCase.KEEP_CASE, expected="HelloWorld"),
]

# Generate test cases for each encrypted message and its corresponding key
test_cases = []
encrypted_messages = [
    dict(message="Mjqqt, Btwqi!", key=5),
    dict(message="Uryyb, Jbeyq!", key=13),
    dict(message="Zwddg, Ogjdv!", key=-8), # same as key=18, testing negative key
]

for encrypted in encrypted_messages:
    for variation in base_variations:
        test_case = variation.copy()
        test_case['message'] = encrypted['message']
        test_case['key'] = encrypted['key']
        test_cases.append(test_case)

@pytest.mark.parametrize("test_params", test_cases)
def test_decryption_permutations(test_client, test_params):
    """Test all permutations of decryption parameters"""
    payload = {
        "message": test_params["message"],
        "key": test_params["key"],
        "keep_spaces": test_params["keep_spaces"],
        "keep_punctuation": test_params["keep_punctuation"],
        "transform_case": test_params["transform_case"].value
    }
    
    response = test_client.post('/decrypt', json=payload)
    assert response.status_code == 200
    assert response.json['success'] == True
    assert response.json['data'] == test_params["expected"]