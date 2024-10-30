from django.db import models


class BaycTransferEvent(models.Model):
    token_id = models.IntegerField(null=False)
    from_address = models.CharField(null=True, max_length=128)
    to_address = models.CharField(null=True, max_length=128)
    transaction_hash = models.CharField(null=True, max_length=128, unique=True, db_index=True)
    block_number = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Check if transaction_hash already exists in the database
        if BaycTransferEvent.objects.filter(transaction_hash=self.transaction_hash).exists():
            return  # Skip saving if duplicate
        super().save(*args, **kwargs)
    