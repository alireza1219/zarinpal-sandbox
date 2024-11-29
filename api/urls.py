from django.urls import path
from .views import PaymentRequestView

urlpatterns = [
    path(
        'pg/rest/WebGate/PaymentRequest.json',
        PaymentRequestView.as_view(),
        name='payment_request'
    ),
]
