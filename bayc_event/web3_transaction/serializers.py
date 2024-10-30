from rest_framework import serializers

from .models import BaycTransferEvent


class BaycTransferSerializer(serializers.ModelSerializer):
    tx_link = serializers.SerializerMethodField()
    
    def get_tx_link(self, obj):
        # Check if obj is a dictionary and extract transaction_hash
        if isinstance(obj, dict):
            transaction_hash = obj.get('transaction_hash')
        else:
            transaction_hash = obj.transaction_hash

        if transaction_hash:
            return f"https://etherscan.io/tx/0x{transaction_hash}"
        return None
    class Meta:
        model = BaycTransferEvent
        fields = "__all__"