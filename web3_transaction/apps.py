import threading

from django.apps import AppConfig


class Web3TransactionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "web3_transaction"