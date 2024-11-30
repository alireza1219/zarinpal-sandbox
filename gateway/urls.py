from django.urls import re_path
from . import views

urlpatterns = [
    re_path(
        r"^pg/StartPay/(?P<authority>[A-Za-z0-9]{36})(/ZarinGate)?/?$",
        views.sandbox_payment_view,
        name="sandbox_payment"
    ),
    re_path(
        r"^pg/Process/$",
        views.sandbox_payment_process_view,
        name="sandbox_payment_process"
    ),
]
