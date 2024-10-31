import sys

from celery import shared_task
from django.conf import settings
from web3 import Web3

from .decorators import handle_exceptions
from .models import BaycTransferEvent

INFURA_URL = f"https://mainnet.infura.io/v3/{settings.INFURA_API_KEY}"
WEB3 = Web3(Web3.HTTPProvider(INFURA_URL))

@handle_exceptions
def get_transfer_by_block(block: str) -> None:
    bayc_contract_address = "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d"
    checksum_address = Web3.to_checksum_address(bayc_contract_address)
    abi = [
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "from",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "to",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "uint256",
                    "name": "tokenId",
                    "type": "uint256",
                },
            ],
            "name": "Transfer",
            "type": "event",
        }
    ]

    contract = WEB3.eth.contract(address=checksum_address, abi=abi)

    print("Listening for events on BAYC...")
    print("Polling for latest transaction")
    sys.stdout.flush()
    
    transfer_filter = contract.events.Transfer().get_logs(from_block=block) # type: ignore
    print(f'Found {len(transfer_filter)} Transfer transactions')
    for event in transfer_filter:
        if event.get("event") != "Transfer":
            raise ValueError("Received event is not a Transfer event.")

        from_address = event["args"]["from"]
        to_address = event["args"]["to"]
        token_id = event["args"]["tokenId"]

        block_number = event["blockNumber"]
        transaction_hash = event["transactionHash"]

        print(f"Saving transaction hash of {transaction_hash.hex()}")
        BaycTransferEvent.objects.create(
            from_address=from_address,
            to_address=to_address,
            token_id=token_id,
            transaction_hash=transaction_hash.hex(),
            block_number=block_number,
        )


@shared_task
def listen_for_events():
    get_transfer_by_block('latest')

  

@shared_task
def catchup_events() -> None:
    # Fetch the latest block number
    print('Running cleanup for today')
    latest_block = WEB3.eth.block_number

    get_transfer_by_block(latest_block - 6500)