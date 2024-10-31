from django.conf import settings
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from web3 import Web3

from .decorators import handle_exceptions
from .models import BaycTransferEvent
from .serializers import BaycTransferSerializer


class BaycTransferViewset(GenericViewSet):
    queryset = BaycTransferEvent.objects.all().order_by("-block_number")
    serializer_class = BaycTransferSerializer

    def get_bayc_transfers(self, request):
        token_id = request.query_params.get("token_id")

        if token_id:
            transfers = self.queryset.filter(token_id=token_id)

            if not transfers.exists():
                raise NotFound(detail="No transfers found for the provided token ID.")
        else:
            transfers = self.queryset.all()

        serializer = self.get_serializer(transfers, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @handle_exceptions
    @action(detail=True, methods=["GET"])
    def get_transfers_by_contract_address(self, request, contract_address):
        # Validate the contract address
        checksum_address = Web3.to_checksum_address(contract_address)
        if not Web3.is_checksum_address(checksum_address):
            return Response(
                {"error": "Invalid contract address."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        infura_url = f"https://mainnet.infura.io/v3/{settings.INFURA_API_KEY}"
        web3 = Web3(Web3.HTTPProvider(infura_url))

        if not web3.is_connected():
            raise ConnectionError("Failed to connect to the Ethereum network.")

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
        contract = web3.eth.contract(address=checksum_address, abi=abi)

        transfer_filter = contract.events.Transfer().get_logs(
            from_block=web3.eth.block_number - 6500
        )
        data = []
        for event in transfer_filter:
            if event.get("event") != "Transfer":
                raise ValueError("Received event is not a Transfer event.")

            transfer_detail = {}
            transfer_detail["from_address"] = event["args"]["from"]
            transfer_detail["to_address"] = event["args"]["to"]
            transfer_detail["token_id"] = event["args"]["tokenId"]

            transfer_detail["block_number"] = event["blockNumber"]
            transaction_hash = event["transactionHash"]
            transfer_detail["transaction_hash"] = transaction_hash.hex()
            data.append(transfer_detail)

        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
