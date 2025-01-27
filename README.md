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

# API information
## Routes
This API serves only two routes:
- `/encrypt`
- `/decrypt`

A 'Hello, World!' smoke test is served on `/` route

## Request & response parameters
All requests are `POST` requests and must include the header `Content-Type: application/json`. All routes take the same parameters:

| **parameter** | **required?** | **type** | **default value** | **description** | **details** |
|---------------|---------------|----------|-------------------|-----------------|-------------|
| `text` | required | `string` | | text to be encrypted, decrypted or hacked | max 5000 chars
| `key` | optional | `integer` | | key for encrypting / decrypting text |
| `keep_spaces` | optional | `boolean` | `True` | whether to keep whitepsace in return string |
| `keep_punctuation` | optional | `boolean` | `True` | whether to keep punctuation in return string |
| `transform_case` | optional | `lowercase`, `uppercase`, `keep_case` | `keep_case` | whether to maintain input case or transform return string to uppercase / lowercase |

All API responses have the following shape:
```JSON
{
    "success": boolean,
    "data": [
        {
            "text": string,
            "key": integer
            // depending on operation,
            // dictionary may contain other key-value pairs
        }
        // ... array may contain many elements
    ] | null,
    "error": {
        "code": string,
        "message": string
    } | null
}
```

### Errors
1. `VALIDATION_ERROR`: Invalid input for request parameter (e.g. passing string to `key` param)
2. `INVALID_KEY`: Key is either 0 or 26, which will not encrypt / decrypt text.

## Operations
This API performs 3 functions: encrypt, decrypt, hack.

### Encryption (`/encrypt` route)

- If `key` is not provided to `/encrypt` route, a random key is generated and used.
- If `key` provided is 0 or a multiple of 26, API will raise an invalid key error.

#### Example POST request
```JSON
{
    "text": "Hello, World!",
    "key": 9,
    "keep_punctuation": false,
    "transform_case": "keep_case"
}
```

#### Example API response
```JSON
{
    "data": [
        {
            "key": 9,
            "text": "Qnuux Fxaum"
        }
    ],
    "error": null,
    "success": true
}
```

### Decryption (`/decrypt` route)

- If `key` is provided to `/decrypt` route, then ciphertext will be derypted with the context that the key provided was the encryption key.
- The `key` in the API response is the decryption key (`encryption key` + `decryption key` = 26).
- Like `/encrypt` route above, if `key` provided is 0 or a multiple of 26, API will raise an invalid key error.


#### Example POST request
```JSON
{
    "text": "Qnuux Fxaum",
    "key": 9,
    "keep_spaces": true,
    "transform_case": "lowercase"
}
```

#### Example API response
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

### Hacking (`/decrypt` route)

- If `key` is NOT provided to `/decrypt` route, then ciphertext will be hacked using frequency analysis.
- A list of possible plaintext solutions will be returned by the API, ordered by best matches first.
- Frequency analysis is best at hacking ciphers longer than 100 characters.

#### Example POST request

```JSON
{
    "text": "R'v qjerwp j panjc crvn nwlahycrwp jwm mnlahycrwp Ljnbja lryqnab frcq cqrb JYR. R fxwmna qxf R ljw kdrum dyxw rc vhbnuo.",
}
```

#### Example API response
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

# Running backend
## Setup
1. Check you have Python 3.11 installed, a specific version number should be returned in the Terminal (e.g. `Python 3.11.11`).
    ```bash
    python3.11 --version
    ```
<br>

2. Navigate to `backend` folder and create an `.env.local` file (copying `.env.example`).
    ``` bash
    cd backend && cp .env.example .env.local
    ```
<br>

## Running backend locally
The backend can be run:
* within a virtual environment or a docker container
* in development or production mode

<br>

From the backend folder, there are 4 ways to run the backend:
| **environment** | **mode** | **command** |
|----------------|----------|--------------|
| virtual env | dev | `./boot.sh venv dev` |
| virtual env | prod | `./boot.sh venv prod` |
| docker | dev | `./boot.sh docker dev` |
| docker | prod | `./boot.sh docker prod` |  

Backend served at [http://localhost:8080](http://localhost:8080) - only route available is 'Hello, World!' smoke test on index route (`/`).
<br><br>




# TESTING
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
