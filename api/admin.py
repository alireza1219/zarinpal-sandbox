from django.contrib import admin
from . import models


@admin.register(models.Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = ['merchant_id', 'created_at']
    list_per_page = 10
    search_fields = ['merchant_id']


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['authority', 'amount', 'description',
                    'status', 'verified', 'reference_id']
    list_per_page = 10
    search_fields = ['authority']
