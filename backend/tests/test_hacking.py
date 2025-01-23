import pytest
from typing import TypedDict

class HackingTestCase(TypedDict):
    plaintext: str
    ciphertext: str
    encryption_key: int

test_cases: list[HackingTestCase] = [
    {
        "plaintext": "The journey of a thousand miles begins with a single step. Keep moving forward, no matter how small the progress may seem. Even the tiniest effort can lead to significant change over time.",
        "ciphertext": "Gur wbhearl bs n gubhfnaq zvyrf ortvaf jvgu n fvatyr fgrc. Xrrc zbivat sbejneq, ab znggre ubj fznyy gur cebterff znl frrz. Rira gur gvavrfg rssbeg pna yrnq gb fvtavsvpnag punatr bire gvzr.",
        "encryption_key": 13
    },
    {
        "plaintext": "In the digital age, protecting sensitive data has become more critical than ever. Encrypting messages is a simple but effective way to ensure information remains secure.",
        "ciphertext": "Rw cqn mrprcju jpn, yaxcnlcrwp bnwbrcren mjcj qjb knlxvn vxan larcrlju cqjw nena. Nwlahycrwp vnbbjpnb rb j brvyun kdc noonlcren fjh cx nwbdan rwoxavjcrxw anvjrwb bnldan.",
        "encryption_key": 9
    },
    {
        "plaintext": "A curious mind is a treasure trove of endless possibilities. Never stop questioning, learning, and exploring the unknown, for each discovery brings new opportunities for growth.",
        "ciphertext": "T vnkbhnl fbgw bl t mkxtlnkx mkhox hy xgwexll ihllbubebmbxl. Gxoxk lmhi jnxlmbhgbgz, extkgbgz, tgw xqiehkbgz max ngdghpg, yhk xtva wblvhoxkr ukbgzl gxp hiihkmngbmbxl yhk zkhpma.",
        "encryption_key": 19
    },
    {
        "plaintext": "From the crackling of the campfire to the whispers of the wind through the trees, nature tells stories that remind us of our connection to the earth and each other.",
        "ciphertext": "Amjh ocz xmvxfgdib ja ocz xvhkadmz oj ocz rcdnkzmn ja ocz rdiy ocmjpbc ocz omzzn, ivopmz ozggn nojmdzn ocvo mzhdiy pn ja jpm xjiizxodji oj ocz zvmoc viy zvxc joczm.",
        "encryption_key": 21
    },
    {
        "plaintext": "Great ideas are like seeds planted in fertile soil. With patience, care, and the right environment, they can grow into something extraordinary, changing the world in ways we never imagined.",
        "ciphertext": "Kviex mhiew evi pmoi wiihw tperxih mr jivxmpi wsmp. Amxl texmirgi, gevi, erh xli vmklx irzmvsrqirx, xlic ger kvsa mrxs wsqixlmrk ibxvesvhmrevc, glerkmrk xli asvph mr aecw ai riziv mqekmrih.",
        "encryption_key": 4
    }
]

@pytest.mark.parametrize("test_params", test_cases)
def test_hack_cipher(test_client, test_params):
    """Test cipher hacking with frequency analysis"""
    payload = {
        "text": test_params["ciphertext"]
    }
    
    response = test_client.post('/decrypt', json=payload)
    assert response.status_code == 200
    assert response.json['success'] == True
    
    solutions = response.json['data']
    
    # Verify solutions are ordered by chi_squared_total
    chi_squared_values = [solution['chi_squared_total'] for solution in solutions]
    assert chi_squared_values == sorted(chi_squared_values)
    
    # Check if correct solution appears in first 5 results
    top_5_solutions = solutions[:5]
    found_match = False
    for solution in top_5_solutions:
        if (solution['text'] == test_params['plaintext'] and 
            solution['key'] + test_params['encryption_key'] == 26):
            found_match = True
            break
    
    assert found_match, "Correct solution not found in top 5 results"
