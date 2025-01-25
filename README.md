Throughout these docs, Terminal commands are provided for Unix shells (i.e. MacOS, Linux).

# Technologies Used

### Frontend

### Backend
- Python 3.11
- Flask
- Pydantic
- pytest
- JSON files
<br><br>

# API requests
This API serves only two routes:
- `/encrypt`
- `/decrypt`

A 'Hello, World!' smoke test is served on `/` route

## Parameters
All requests are `POST` requests and must include the header `Content-Type: application/json`. All routes take the same parameters:

| **parameter** | **required?** | **type** | **default value** | **description** | **details** |
|---------------|---------------|----------|-------------------|-----------------|-------------|
| `text` | required | `string` | | text to be encrypted, decrypted or hacked | max 5000 chars
| `key` | optional | `integer` | | key for encrypting / decrypting text |
| `keep_spaces` | optional | `boolean` | `True` | whether to keep whitepsace in return string |
| `keep_punctuation` | optional | `boolean` | `True` | whether to keep punctuation in return string |
| `transform_case` | optional | `lowercase`, `uppercase`, `keep_case` | `keep_case` | whether to maintain input case or transform return string to uppercase / lowercase |

## Operations
### Encryption (`/encrypt` route)

- If `key` is not provided to `/encrypt` route, a random key is generated and used.
- If `key` provided is 0 or a multiple of 26, API will raise an invalid key error.

#### Example POST request for Encryption operation
```JSON
{
    "text": "Hello world",
    "key": 9,
    "keep_punctuation": false,
    "transform_case": "keep_case"
}
```

### Decryption (`/decrypt` route)

- If `key` is provided to `/decrypt` route, then ciphertext will be derypted using that one specific key.
- Like `/encrypt` route above, if `key` provided is 0 or a multiple of 26, API will raise an invalid key error.

#### Example POST request for Decryption operation
```JSON
{
    "text": " ", # add hello world, shifted by key of 9
    "key": 17,
    "keep_spaces": true,
    "transform_case": "lowercase"
}
```

### Hacking (`/decrypt` route)

- If `key` is NOT provided to `/decrypt` route, then ciphertext will be hacked using frequency analysis.
- A list of possible plaintext solutions will be returned by the API, ordered by best matches first.
- Frequency analysis is best at hacking ciphers longer than 100 characters.

#### Example POST request for Hacking operation

```JSON
{
    "text": "R'v qjerwp j panjc crvn nwlahycrwp jwm mnlahycrwp Ljnbja lryqnab frcq cqrb JYR. R fxwmna qxf R ljw kdrum dyxw rc vhbnuo.",
}
```

# API responses

## Shape of API response
All API responses have the following shape:
```JSON
{
    "success": boolean,
    "data": array | null,
    "error": {
        "code": string,
        "message": string
    } | null
}
```

#### Example API response for Encryption operation (following example above)
```JSON
{
    "data": [
        {
            "key": 9,
            "text": "Qnuux fxaum"
        }
    ],
    "error": null,
    "success": true
}
```

#### Example API response for Decyption operation (following example above)
```JSON
{
    "data": [
        {
            "key": 17,
            "text": "hello world"
        }
    ],
    "error": null,
    "success": true
}
```

#### Example API response for Hacking operation
```JSON
{
    "data": [
        {
            "chi_squared_total": 1063.8706,
            "key": 17,
            "text": "I'm having a great time encrypting and decrypting Caesar ciphers with this API. I wonder how I can build upon it myself."
        },
        {
            "chi_squared_total": 11957.0633,
            "key": 2,
            "text": "T'x slgtyr l rcple etxp pyncjaetyr lyo opncjaetyr Nlpdlc ntaspcd htes estd LAT. T hzyopc szh T nly mftwo fazy te xjdpwq."
        },
        {
            "chi_squared_total": 18062.1299,
            "key": 15,
            "text": "G'k fytgle y epcyr rgkc clapwnrgle ylb bcapwnrgle Aycqyp agnfcpq ugrf rfgq YNG. G umlbcp fmu G ayl zsgjb snml gr kwqcjd."
        },
        {
            "chi_squared_total": 18557.1665,
            "key": 5,
            "text": "W'a vojwbu o ufsoh hwas sbqfmdhwbu obr rsqfmdhwbu Qosgof qwdvsfg kwhv hvwg ODW. W kcbrsf vck W qob piwzr idcb wh amgszt."
        },
        {
            "chi_squared_total": 20707.5345,
            "key": 24,
            "text": "P't ohcpun h nylha aptl lujyfwapun huk kljyfwapun Jhlzhy jpwolyz dpao aopz HWP. P dvukly ovd P jhu ibpsk bwvu pa tfzlsm."
        }
        // ... 20 more solutions (omitted for brevity)
    ],
    "error": null,
    "success": true
}
```

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