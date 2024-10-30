# from django.apps import AppConfig
# import threading
# from .views import listen_for_events 

# class Web3TransactionConfig(AppConfig):
#     default_auto_field = "django.db.models.BigAutoField"
#     name = "web3_transaction"
    
#     def ready(self):
#         # Start the test function in a separate thread
#         threading.Thread(target=listen_for_events, daemon=True).start()


import threading

# web3_transaction/apps.py
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class Web3TransactionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web3_transaction'

    def ready(self):
        # Connect the signal to start the test function after migrations
        from .tasks import listen_for_events
        threading.Thread(target=listen_for_events, daemon=True).start()
