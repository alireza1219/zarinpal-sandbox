from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator


class Merchant(models.Model):
    merchant_id = models.CharField(max_length=36, unique=True, validators=[
        MinLengthValidator(
            limit_value=36,
            message='The merchant id must be at least 36 characters.'
        ),
        MaxLengthValidator(
            limit_value=36,
            message='The merchant id must not be greater than 36 characters.'
        ),
    ],)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.merchant_id)


class Transaction(models.Model):
    PENDING = 'P'
    SUCCESS = 'S'
    FAILED = 'F'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (SUCCESS, 'Success'),
        (FAILED, 'Failed'),
    ]

    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    authority = models.CharField(max_length=36, unique=True)
    amount = models.PositiveIntegerField()
    callback_url = models.URLField()
    description = models.CharField(max_length=255)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=PENDING)
    verified = models.BooleanField(default=False)
    reference_id = models.CharField(
        max_length=36, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.authority)
