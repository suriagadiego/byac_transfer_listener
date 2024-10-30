import sys
import time

from django.conf import settings
from web3 import Web3

from .decorators import handle_exceptions
from .models import BaycTransferEvent


@handle_exceptions
def listen_for_events():
    infura_url = f"https://mainnet.infura.io/v3/{settings.INFURA_API_KEY}"
    web3 = Web3(Web3.HTTPProvider(infura_url))

    bayc_contract_address = "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d"
    checksum_address = Web3.to_checksum_address(bayc_contract_address)
    abi = [
        {
            "anonymous": False,
            "inputs": [
                {"indexed": True, "internalType": "address", "name": "from", "type": "address"},
                {"indexed": True, "internalType": "address", "name": "to", "type": "address"},
                {"indexed": True, "internalType": "uint256", "name": "tokenId", "type": "uint256"},
            ],
            "name": "Transfer",
            "type": "event",
        }
    ]

    contract = web3.eth.contract(address=checksum_address, abi=abi)

    print('Listening for events on BAYC...')
    sys.stdout.flush()

    while True:
        print('Polling for latest transaction')
        
        try:
            transfer_filter = contract.events.Transfer().get_logs(from_block='latest')
            
            for event in transfer_filter:
                if event.get("event") != "Transfer":
                    raise ValueError("Received event is not a Transfer event.")


                from_address = event["args"]["from"]
                to_address = event["args"]["to"]
                token_id = event["args"]["tokenId"]

                block_number = event["blockNumber"]
                transaction_hash = event["transactionHash"]

                print(f'Saving transaction hash of {transaction_hash.hex()}')

                BaycTransferEvent.objects.create(
                    from_address=from_address,
                    to_address=to_address,
                    token_id=token_id,
                    transaction_hash=transaction_hash.hex(),
                    block_number=block_number,
                )
        
        except Exception as e:
            print(f"An error occurred while processing events: {e}")
            sys.stdout.flush()

        time.sleep(2)  # Poll every 2 seconds