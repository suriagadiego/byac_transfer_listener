# BAYC NFT Transfer Event Listener

## Description
The BAYC NFT Transfer Event Listener is a Django application that connects to the Ethereum blockchain via Infura to listen for and record transfer events of Bored Ape Yacht Club (BAYC) NFTs. This application enables users to monitor transfer events in real time and provides an API for accessing transfer history for specific tokens.

## Features
- Connects to the Ethereum mainnet via Infura.
- Listens for transfer events from the BAYC smart contract.
- Stores transfer event data in a SQLite database.
- Exposes a simple API endpoint to retrieve transfer history for a specific token ID.

## Technologies Used
- **Django**: Web framework for building the application.
- **Web3.py**: Python library for interacting with the Ethereum blockchain.
- **SQLite**: Database for storing transfer event data.
- **Celery & Redis**: Workers for handling the event listener

## Installation

### Prerequisites
- Python 3.x
- pip (Python package installer)
- brew
- redis

### Steps to Install & Running the Event Listener
1. Clone the repository:
   ```bash
   git clone https://github.com/suriagadiego/byac_transfer_listener.git
   cd bayc-event-listener
    ```

2. Install  app requirements:
    ```bash
    pip install -r requirements.txt
    ```

3. Install Redis via Brew (for unix systems) <br>
    **REDIS IS REQUIRED TO RUN THIS APP**
    ```bash
    brew install redis
    ```

4. Create an env file on the root of the project
   ```bash
   INFURA_API_KEY=sample_api_key1
   ```

5. Run the celery Workers and the project:
    ```bash
    celery -A bayc_event worker -E -l info
    ```

    in another terminal run the celery beat
    ```bash
    celery -A bayc_event beat --loglevel=info
    ```

    in yet another terminal run the server
    ```bash
    python manage.py runserver
    ```


### Note
To monitor the SQLite database, you can use **DBeaver**. Ensure to set up a connection to the SQLite database in your project to visualize and manage the stored transfer events effectively.


## Endpoints

### Get Transfer History of BAYC
- **URL**: `/transfers/<token_id>/`
- **Method**: `GET`
- **Description**: Retrieves the transfer history for a specific token ID.
- **URL Params**: 
  - `token_id`: The ID of the token for which you want to retrieve transfer history.
- **Success Response**:
  - **Code**: 200
  - **Content**: 
  ```json
  {
    "transfers": [
      {
        "token_id": "123",
        "from_address": "0xabcdef...",
        "to_address": "0x123456...",
        "transaction_hash": "0x7890...",
        "tx_link": "https://etherscan.io/tx/0x{transaction_hash}",
        "block_number": 456789,
        "created_at": "2024-10-31T10:00:00Z"
      },
      ...
    ]
  }

- **Error Response**
  - **Code**: 404
  - **Content**: 
  ```json
  {
    "error": "Token ID not found."
  }
  ```

### Example Request
To get the transfer history for a specific token ID:

```http
GET http://127.0.0.1:8000/web3_transaction/bayc/transfers/?token_id=123
```

To get the transfer history without specifying a token ID:
```http
GET http://127.0.0.1:8000/web3_transaction/contract_address/<str:contract_address>/
```

### Get Transfer History of a certain contract address
- **URL**: `/transfers/<token_id>/`
- **Method**: `GET`
- **Description**: Retrieves the transfer history of a specific contract address, queries it directly from the chain not in the db
- **Query Params**: 
  - `contract_address`: The contract address of which you want to retrieve transfer history.
- **Success Response**:
  - **Code**: 200
  - **Content**: 
  ```json
  {
    "transfers": [
      {
        "token_id": "123",
        "from_address": "0xabcdef...",
        "to_address": "0x123456...",
        "transaction_hash": "0x7890...",
        "tx_link": "https://etherscan.io/tx/0x{transaction_hash}",
        "block_number": 456789,
        "created_at": "2024-10-31T10:00:00Z"
      },
      ...
    ]
  }

- **Error Response**
  - **Code**: 404
  - **Content**: 
  ```json
  {
    "error": "Contract address not Valid."
  }
  ```

### Example Request
To get the transfer history for a specific Contract address:
```http
GET http://127.0.0.1:8000/web3_transaction/contract_address/<str:contract_address>/
```

## Highlights
- The application is polling the latest blocks on the Ethereum blockchain using **Celery**, **Celery Beat**, and **Redis**. 
- It polls for new transfer events every 30 seconds using Celery Beat to ensure timely updates.
- Additionally, a cron job is scheduled on Celery Beat to run every 24 hours at 4 PM UTC, performing a cleanup of large blocks to ensure that no events are missed during the regular polling.


## Simplifications made
- Currently this is deployed in this domain 
```http
https://byactransferlistener-production.up.railway.app/web3_transaction/bayc/transfers/
```
- Unfortunately due to timeconstraints the celery workers are not yet deployed. Will also deploy the celery workers in the future if needed

# Author
[Diego Suriaga] - [GitHub Profile](https://github.com/suriagadiego)
