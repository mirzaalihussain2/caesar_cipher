import pytest
from app.routes.encrypt import TransformCase

test_cases = [
    # key=5 permutations
    dict(key=5, keep_spaces=True, keep_punctuation=True, transform_case=TransformCase.LOWERCASE, expected="mjqqt, btwqi!"),  # 0
    dict(key=5, keep_spaces=True, keep_punctuation=True, transform_case=TransformCase.UPPERCASE, expected="MJQQT, BTWQI!"),  # 1
    dict(key=5, keep_spaces=True, keep_punctuation=True, transform_case=TransformCase.KEEP_CASE, expected="Mjqqt, Btwqi!"),  # 2
    dict(key=5, keep_spaces=True, keep_punctuation=False, transform_case=TransformCase.LOWERCASE, expected="mjqqt btwqi"),  # 3
    dict(key=5, keep_spaces=True, keep_punctuation=False, transform_case=TransformCase.UPPERCASE, expected="MJQQT BTWQI"),  # 4
    dict(key=5, keep_spaces=True, keep_punctuation=False, transform_case=TransformCase.KEEP_CASE, expected="Mjqqt Btwqi"),  # 5
    dict(key=5, keep_spaces=False, keep_punctuation=True, transform_case=TransformCase.LOWERCASE, expected="mjqqt,btwqi!"),  # 6
    dict(key=5, keep_spaces=False, keep_punctuation=True, transform_case=TransformCase.UPPERCASE, expected="MJQQT,BTWQI!"),  # 7
    dict(key=5, keep_spaces=False, keep_punctuation=True, transform_case=TransformCase.KEEP_CASE, expected="Mjqqt,Btwqi!"),  # 8
    dict(key=5, keep_spaces=False, keep_punctuation=False, transform_case=TransformCase.LOWERCASE, expected="mjqqtbtwqi"),  # 9
    dict(key=5, keep_spaces=False, keep_punctuation=False, transform_case=TransformCase.UPPERCASE, expected="MJQQTBTWQI"),  # 10
    dict(key=5, keep_spaces=False, keep_punctuation=False, transform_case=TransformCase.KEEP_CASE, expected="MjqqtBtwqi"),  # 11
    
    # key=13 permutations
    dict(key=13, keep_spaces=True, keep_punctuation=True, transform_case=TransformCase.LOWERCASE, expected="uryyb, jbeyq!"),  # 12
    dict(key=13, keep_spaces=True, keep_punctuation=True, transform_case=TransformCase.UPPERCASE, expected="URYYB, JBEYQ!"),  # 13
    dict(key=13, keep_spaces=True, keep_punctuation=True, transform_case=TransformCase.KEEP_CASE, expected="Uryyb, Jbeyq!"),  # 14
    dict(key=13, keep_spaces=True, keep_punctuation=False, transform_case=TransformCase.LOWERCASE, expected="uryyb jbeyq"),  # 15
    dict(key=13, keep_spaces=True, keep_punctuation=False, transform_case=TransformCase.UPPERCASE, expected="URYYB JBEYQ"),  # 16
    dict(key=13, keep_spaces=True, keep_punctuation=False, transform_case=TransformCase.KEEP_CASE, expected="Uryyb Jbeyq"),  # 17
    dict(key=13, keep_spaces=False, keep_punctuation=True, transform_case=TransformCase.LOWERCASE, expected="uryyb,jbeyq!"),  # 18
    dict(key=13, keep_spaces=False, keep_punctuation=True, transform_case=TransformCase.UPPERCASE, expected="URYYB,JBEYQ!"),  # 19
    dict(key=13, keep_spaces=False, keep_punctuation=True, transform_case=TransformCase.KEEP_CASE, expected="Uryyb,Jbeyq!"),  # 20
    dict(key=13, keep_spaces=False, keep_punctuation=False, transform_case=TransformCase.LOWERCASE, expected="uryybjbeyq"),  # 21
    dict(key=13, keep_spaces=False, keep_punctuation=False, transform_case=TransformCase.UPPERCASE, expected="URYYBJBEYQ"),  # 22
    dict(key=13, keep_spaces=False, keep_punctuation=False, transform_case=TransformCase.KEEP_CASE, expected="UryybJbeyq"),  # 23
    
    # key=18 permutations
    dict(key=18, keep_spaces=True, keep_punctuation=True, transform_case=TransformCase.LOWERCASE, expected="zwddg, ogjdv!"),  # 24
    dict(key=18, keep_spaces=True, keep_punctuation=True, transform_case=TransformCase.UPPERCASE, expected="ZWDDG, OGJDV!"),  # 25
    dict(key=18, keep_spaces=True, keep_punctuation=True, transform_case=TransformCase.KEEP_CASE, expected="Zwddg, Ogjdv!"),  # 26
    dict(key=18, keep_spaces=True, keep_punctuation=False, transform_case=TransformCase.LOWERCASE, expected="zwddg ogjdv"),  # 27
    dict(key=18, keep_spaces=True, keep_punctuation=False, transform_case=TransformCase.UPPERCASE, expected="ZWDDG OGJDV"),  # 28
    dict(key=18, keep_spaces=True, keep_punctuation=False, transform_case=TransformCase.KEEP_CASE, expected="Zwddg Ogjdv"),  # 29
    dict(key=18, keep_spaces=False, keep_punctuation=True, transform_case=TransformCase.LOWERCASE, expected="zwddg,ogjdv!"),  # 30
    dict(key=18, keep_spaces=False, keep_punctuation=True, transform_case=TransformCase.UPPERCASE, expected="ZWDDG,OGJDV!"),  # 31
    dict(key=18, keep_spaces=False, keep_punctuation=True, transform_case=TransformCase.KEEP_CASE, expected="Zwddg,Ogjdv!"),  # 32
    dict(key=18, keep_spaces=False, keep_punctuation=False, transform_case=TransformCase.LOWERCASE, expected="zwddgogjdv"),  # 33
    dict(key=18, keep_spaces=False, keep_punctuation=False, transform_case=TransformCase.UPPERCASE, expected="ZWDDGOGJDV"),  # 34
    dict(key=18, keep_spaces=False, keep_punctuation=False, transform_case=TransformCase.KEEP_CASE, expected="ZwddgOgjdv")  # 35
]

@pytest.mark.parametrize("test_params", test_cases)
def test_encryption_permutations(test_client, test_params):
    """Test all permutations of encryption parameters"""
    payload = {
        "message": "Hello, World!",
        "key": test_params["key"],
        "keep_spaces": test_params["keep_spaces"],
        "keep_punctuation": test_params["keep_punctuation"],
        "transform_case": test_params["transform_case"].value
    }
    
    response = test_client.post('/encrypt', json=payload)
    assert response.status_code == 200
    assert response.json['success'] == True
    assert response.json['data'] == test_params["expected"]