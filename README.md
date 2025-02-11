# Overview
This is a basic app that encrypts, decrypts and hacks Caesar ciphers. It uses frequency analysis: comparing frequencies of letters and bigrams in the ciphertext to frequencies in normal English language.
<br><br>

# Technologies Used
Throughout these docs, Terminal commands are provided for Unix shells (i.e. MacOS, Linux).

## Frontend
- Next.js 15.1
- React 19
- TypeScript
- TailwindCSS
- shadcn/ui components

## Backend
- Python 3.11
- Flask
- Pydantic
- pytest
- Python's statistics module
- JSON files
<br><br>

# API information

## Routes
The backend API serves only two routes:
- `/encrypt`
- `/decrypt`

For understanding the backend structure, begin with the [@encrypt.py](backend/app/encrypt.py) and [@decrypt.py](backend/app/decrypt.py) files that correspond to these routes.
<br><br>

#### Smoke test
* 'Hello, World!' smoke test served on `/` route.
<br><br>

## Request & response parameters
All requests are `POST` requests and must include the header `Content-Type: application/json`. All routes take the same parameters:

| **parameter** | **required?** | **type** | **default value** | **description** | **details** |
|---------------|---------------|----------|-------------------|-----------------|-------------|
| `text` | required | `string` | | text to be encrypted, decrypted or hacked | max 10,000 chars
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
            // ...
        }
        // ... array may contain many elements
    ] | null,
    "error": {
        "code": string,
        "message": string
    } | null,
    "metadata": {
        "action": 'encrypt', // could be 'decrypt' or 'hack'
        "key": integer
        // ...
    } | null
}
```

### Errors
1. `VALIDATION_ERROR`: Invalid input for request parameter (e.g. passing string to `key` param)
2. `INVALID_KEY`: Key is either 0 or 26, which will not encrypt / decrypt text.
<br><br>

## Operations
This API performs 3 functions: **encrypt**, **decrypt**, **hack**.

### Encryption (`/encrypt` route)

- If `key` is not provided to `/encrypt` route, a random key is generated and used.
- If `key` provided is 0 or a multiple of 26, API will raise an invalid key error.

#### Example POST request (using Postman)
```JSON
{
    "text": "Hello, World!",
    "key": 9,
    "keep_punctuation": false,
    "transform_case": "keep_case"
}
```

#### Example POST request (using cURL)
```bash
curl -X POST http://localhost:8080/encrypt \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, World!",
    "key": 9,
    "keep_punctuation": false,
    "transform_case": "keep_case"
  }'

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
        "action": "encrypt",
        "key": 9
    }
}
```

### Decryption (`/decrypt` route)

- If `key` is provided to `/decrypt` route, then ciphertext will be derypted with the context that the key provided was the encryption key.
- The `key` in the API response is the decryption key (`encryption key` + `decryption key` = 26).
- Like `/encrypt` route above, if `key` provided is 0 or a multiple of 26, API will raise an invalid key error.

#### Example POST request (using Postman)
```JSON
{
    "text": "Qnuux Fxaum",
    "key": 9,
    "keep_spaces": true,
    "transform_case": "lowercase"
}
```

#### Example POST request (using cURL)
```bash
curl -X POST http://localhost:8080/decrypt \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Qnuux Fxaum",
    "key": 9,
    "keep_spaces": true,
    "transform_case": "lowercase"
  }'
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
        "action": "decrypt",
        "key": 17
    }
}
```

### Hacking (`/decrypt` route)

- If `key` is NOT provided to `/decrypt` route, then ciphertext will be hacked using frequency analysis.
- A list of possible plaintext solutions will be returned by the API, ordered by best matches first.
- Frequency analysis is best at hacking ciphers longer than 100 characters.
- For ciphertexts longer than 2000 characters, analysis is run on the first 2000 characters and then repeated on ciphertexts of increasing length until the full ciphertext is used or we have high confidence decryption was successful.

#### Example POST request (using Postman)
```JSON
{
    "text": "R'v qjerwp j panjc crvn nwlahycrwp jwm mnlahycrwp Ljnbja lryqnab frcq cqrb JYR. R fxwmna qxf R ljw kdrum dyxw rc vhbnuo."
}
```

#### Example POST request (using cURL)
```bash
curl -X POST http://localhost:8080/decrypt \
  -H "Content-Type: application/json" \
  -d '{
    "text": "R'\''v qjerwp j panjc crvn nwlahycrwp jwm mnlahycrwp Ljnbja lryqnab frcq cqrb JYR. R fxwmna qxf R ljw kdrum dyxw rc vhbnuo."
  }''
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
        "action": "hack",
        "analysis_length": 120,
        "confidence_level": "low",
        "key": 17 // key of best match
    }
}
```
<br>

# Running backend

## Setup
1. Check you have Python 3.11 installed, a specific version number should be returned in the Terminal (e.g. `Python 3.11.11`).
    ```bash
    python3.11 --version
    ```
<br>

2. Navigate to `backend` folder and create an `.env.local` file (copying `.env.example`).
    ```bash
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
|-----------------|----------|-------------|
| virtual env | dev | `./boot.sh venv dev` |
| virtual env | prod | `./boot.sh venv prod` |
| docker | dev | `./boot.sh docker dev` |
| docker | prod | `./boot.sh docker prod` |  

Backend served at [http://localhost:8080](http://localhost:8080) - only route available is 'Hello, World!' smoke test on index route (`/`).

## Running frontend
1. Ensure you have Node 22+ installed
    ```bash
    node --version
    ```

2. Navigate to `frontend` folder and create an `.env.local` file (copying `.env.example`).
    ```bash
    cd frontend && cp .env.example .env.local
    ```

3. Install dependencies with `pnpm install`
4. Run development server with `pnpm dev`
5. Frontend served at [http://localhost:3000](http://localhost:3000).
<br><br>

# Testing
There is a simple suite of API integration tests that test each operation (encryption, decryption, and hacking) end-to-end with various permutations. If any of the specific functions required for these 3 broader operations start to fail, these failure should be reflected in the API tests.

- **Encryption Tests**: Tests encrypting the same 'Hello, World!' text with 3 different keys and all permutations of `keep_spaces`, `keep_punctuation` and `transform_case`.
- **Decryption Tests**: Tests decrypting 'Hello, World!' ciphertext, encrypted with 3 different keys and all permutations of `keep_spaces`, `keep_punctuation` and `transform_case`.
- **Hacking Tests**: Tests hacking 12 ciphertexts (5 ciphertexts < 200 characters, 6 ciphertexts 2000 - 4000 characters, 1 ciphertext > 9000 characters). Checks that metadata includes a confidence level (high, medium, low) and the length of analysed text
- **Basic Smoke Test**: Verifies API is running & responding.

All tests interact with the API through HTTP requests.

## Running API tests
1. Set up backend following ([setup](#setup)) instructions above.
2. Once in `backend` folder, execute `./test.sh` from Terminal

    | **testing mode** |  **command** |
    |------------------|--------------|
    | running tests normally |  `./test.sh` |
    | running tests with coverage report |  `./test.sh coverage` |
    | running tests with detailed output |  `./test.sh verbose` |

## Running E2E frontend tests
Not yet implemented (will likely use Playwright)
<br><br>

# Deployment
## Requirements for running backend locally
* The following files are used for running the backend locally using a virtual environment (in `dev` or `prod` modes):
    * [boot.sh](/backend/boot.sh)
    * [config.py](/backend/config.py)
    * env files (`.env.local` / `.env.prod`)

* The following files are used for running the backend locally using a docker container (in `dev` and `prod` modes):
    * [config.py](/backend/config.py)
    * env files (`.env.local`, `.env.prod`)
    * docker compose files (dev: [docker-compose.yml](/backend/docker-compose.yml) / prod: [docker-compose.prod.yml](/backend/docker-compose.yml))
    * dockerfile ([Dockerfile.dev](/backend/Dockerfile.dev) / [Dockerfile.prod](/backend/Dockerfile.prod))

NOTE: [boot.sh](/backend/boot.sh) not required for running backend using docker, because we only use the `docker compose` commands at the very end of the file.
<br><br>

## Requirements for deployment
Deployment information correct as of 31 Jan 2025.

### Railway
The backend can be deployed to [Railway](https://railway.com) with the following files:
* [config.py](/backend/config.py)
* dockerfile ([Dockerfile.prod](/backend/Dockerfile.prod))
<br><br>

NOTE:
1. if pushing as a monorepo, set root directory to `/backend`
2. if not automatically detected, set variable to `RAILWAY_DOCKERFILE_PATH` to `backend/Dockerfile.prod`
3. set other variables from `.env.prod` file
<br><br>


## TO DO LIST
- long-term, do I want types in a shared JSON, accessible to both front- & back-end? Rather than having duplicated types in both frontend & backend, and keeping both in sync.

### frontend
- add frontend E2E tests, maybe in Playwright
- for 'Hack' need an option to loop through solutions (i.e. try again), esp when confidence_level !== high
- light & dark mode
- Add .nvmrc file for controlling node / nvm version

### backend
- backend runs CORS in prod, security vulnerability, change in future
