from django.db import models


class BaycTransferEvent(models.Model):
    token_id = models.IntegerField(null=False)  # type: ignore
    from_address = models.CharField(null=True, max_length=128)  # type: ignore
    to_address = models.CharField(null=True, max_length=128)  # type: ignore
    transaction_hash = models.CharField(null=True, max_length=128, unique=True, db_index=True)  # type: ignore
    block_number = models.IntegerField(null=True)  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True)  # type: ignore

    def save(self, *args, **kwargs):
        # Check if transaction_hash already exists in the database
        if BaycTransferEvent.objects.filter(
            transaction_hash=self.transaction_hash
        ).exists():
            return  # Skip saving if duplicate
        super().save(*args, **kwargs)
