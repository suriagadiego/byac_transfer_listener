from django.urls import path

from . import views

urlpatterns = [
    path(
        "bayc/transfers/",
        views.BaycTransferViewset.as_view({"get": "get_bayc_transfers"}),
        name="get_bayc_transfers",
    ),
    path(
        "contract_address/<str:contract_address>/",
        views.BaycTransferViewset.as_view({"get": "get_transfers_by_contract_address"}),
        name="get_transactions_by_address",
    ),
]
