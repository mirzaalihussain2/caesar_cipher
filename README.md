Throughout these docs, Terminal commands are provided for Unix shells (i.e. MacOS, Linux).

# Technologies Used

### Backend
- Python 3.11
- Flask
- Pydantic
- pytest
<br><br>


This API serves two routes:
- `/encrypt`
- `/decrypt`

Each route consumes POST requests and can take the following parameters:
- `text` - required - string, max length: 5000 characters
- `key` - optional - integer, no default value
- `keep_spaces` - optional - boolean, default: True, determines whether to keep whitespace in the return string
- `keep_punctuation` - optional - boolean, default: True, determines whether to keep punctuation in the return string
- `transform case` - optional - 'lowercase' | 'uppercase' | 'keep_case', default: 'keep_case' - determine whether to maintain input case or transform return string to upper- or lower-case.

^ re-write this as a table

Example POST request to `/encrypt` route
{
    "text": "Hello world",
    "key": 9,
    "keep_punctuation": false,
    "transform_case": "keep_case"
}
- if `key` is not provided to `/encrypt` route, a random key will be generated
- if `key` is 0 or a multiple of 26, this will raise an invalid key error

Example decryption POST request to `/decrypt` route
- if `key` is provided on `/decrypt`, then simple decryption using that one specific key
- if `key` is not provided


TESTS
- Tests for all 3 operations: encryption, decryption and hacking. Encryption & decryption also include lots of variations of transforming the text (e.g. keeping or removing spaces, keeping or removing space, keeping or changing the case).
- Didn't do unit tests for specific functions, as all those functions are required to work for the API tests to work. So if specific functions fail, this'll be reflected in API tests failing for our routes.

# caesar_cipher
Caesar cipher encrypter and decrypter. Decrypter uses letter frequencies in English language to suggest decrypted text.

## TO DO
- Deploy
- Write READ.ME explaining the two routes, 3 operations (encrypt, decrypt, hack)
- Add to READ.ME explaining running & deploying backend
- imoplement frontend

- for longer strings, a strategy would be to calculate key on a substring and then apply that key to rest of string - for a 5000 char string, find correct key on 1000 char string and then apply to rest of string