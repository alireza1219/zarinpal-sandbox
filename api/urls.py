from django.urls import path
from . import views

urlpatterns = [
    path(
        'pg/rest/WebGate/PaymentRequest.json',
        views.PaymentRequestView.as_view(),
        name='payment_request'
    ),
    path(
        'pg/rest/WebGate/PaymentVerification.json',
        views.PaymentVerificationView.as_view(),
        name='payment_verification'
    ),
]
