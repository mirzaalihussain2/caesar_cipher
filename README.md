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
            // hacking operation also returns key and chi_squared value
        }
        // ... array may contain many elements
    ] | null,
    "error": {
        "code": string,
        "message": string
    } | null,
    "metadata": {
        "key": integer
        // hacking operation also returns confidence_level and analysis_length
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
            "text": "Qnuux Fxaum"
        }
    ],
    "error": null,
    "success": true,
    "metadata": {
        "key": 9
    }
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
            "text": "hello world"
        }
    ],
    "error": null,
    "success": true,
    "metadata": {
        "key": 17
    }
}
```

### Hacking (`/decrypt` route)

- If `key` is NOT provided to `/decrypt` route, then ciphertext will be hacked using frequency analysis.
- A list of possible plaintext solutions will be returned by the API, ordered by best matches first.
- Frequency analysis is best at hacking ciphers longer than 100 characters.
- For ciphertexts longer than 2000 characters, analysis is run on the first 2000 characters and then repeated on ciphertexts of increasing length until the full ciphertext is used or we have high confidence decryption was successful.

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
            "chi_squared_total": 27.43352,
            "key": 17,
            "text": "I'm having a great time encrypting and decrypting Caesar ciphers with this API. I wonder how I can build upon it myself."
        },
        {
            "chi_squared_total": 311.42947,
            "key": 2,
            "text": "T'x slgtyr l rcple etxp pyncjaetyr lyo opncjaetyr Nlpdlc ntaspcd htes estd LAT. T hzyopc szh T nly mftwo fazy te xjdpwq."
        },
        {
            "chi_squared_total": 366.69404,
            "key": 15,
            "text": "G'k fytgle y epcyr rgkc clapwnrgle ylb bcapwnrgle Aycqyp agnfcpq ugrf rfgq YNG. G umlbcp fmu G ayl zsgjb snml gr kwqcjd."
        },
        {
            "chi_squared_total": 465.21693,
            "key": 5,
            "text": "W'a vojwbu o ufsoh hwas sbqfmdhwbu obr rsqfmdhwbu Qosgof qwdvsfg kwhv hvwg ODW. W kcbrsf vck W qob piwzr idcb wh amgszt."
        },
        {
            "chi_squared_total": 502.72844,
            "key": 19,
            "text": "K'o jcxkpi c itgcv vkog gpetarvkpi cpf fgetarvkpi Ecguct ekrjgtu ykvj vjku CRK. K yqpfgt jqy K ecp dwknf wrqp kv oaugnh."
        },
        // ... 20 more solutions (omitted for brevity)
    ],
    "error": null,
    "success": true,
    "metadata": {
        "analysis_length": 120,
        "confidence_level": "low",
        "key": 17 // key of best match
    },
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

# Testing
There is a simple suite of API integration tests that test each operation (encryption, decryption, and hacking) end-to-end with various permutations. If any of the specific functions required for these 3 broader operations start to fail, these failure should be reflected in the API tests.

- **Encryption Tests**: Tests encrypting the same 'Hello, World!' text with 3 different keys and all permutations of `keep_spaces`, `keep_punctuation` and `transform_case`.
- **Decryption Tests**: Tests decrypting 'Hello, World!' ciphertext, encrypted with 3 different keys and all permutations of `keep_spaces`, `keep_punctuation` and `transform_case`.
- **Hacking Tests**: Tests hacking 12 ciphertexts (5 ciphertexts < 200 characters, 6 ciphertexts 2000 - 4000 characters, 1 ciphertext > 9000 characters). Checks that metadata includes a confidence level (high, medium, low) and the length of analysed text
- **Basic Smoke Test**: Verifies API is running & responding.

All tests interact with the API througuh HTTP requests.

## Running tests
1. Set up backend following ([setup](#setup)) instructions above.
2. Once in `backend` folder, execute `./test.sh` from Terminal

    | **testing mode** |  **command** |
    |------------------|--------------|
    | running tests normally |  `./test.sh` |
    | running tests with coverage report |  `./test.sh coverage` |
    | running tests with detailed output |  `./test.sh verbose` |
<br>




# caesar_cipher
Caesar cipher encrypter and decrypter. Decrypter uses letter frequencies in English language to suggest decrypted text.

deployed to railway - need to write about how to deploy?

## TO DO
- Write READ.ME explaining the two routes, 3 operations (encrypt, decrypt, hack)
- Add to READ.ME explaining running & deploying backend
- imoplement frontend


- testing API locally without POSTMAN (or explain both, POSTMAN & CURL)

tests for errors:
    - on encrypt / decrypt
        - TEXT: text > 5000 characters --> VALIDATION ERROR
        - TEXT: text missing, only key provided
        - KEY: providing a key that's a float --> VALIDATION ERROR
        - KEY: invalid key error, when 0
        - KEY: invalid key error, when 26
        - keep_spaces: provide string, validation error
        - keep_punctuation: provide int, validation error
        - transform_case: "UPPERCASE"

    - on hacking test
        - Empty 'text' string, code: VALIDATION_ERROR

- add 'confidence_score' for longer strings (e.g. 1000 chars or more, maybe 2000 chars or more)


- add a section explain confidence intervals
maybe include this in file actually, rather than here?
    # separation_score is a Z-statistic adapted for frequency analysis whwere chi-squared stats are NOT expected to be normally distributed,
    # separation_score compares lowest value against second lowest value rather than mean