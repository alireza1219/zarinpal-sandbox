from rest_framework.views import APIView
from . import models, helpers, validators


class PaymentRequestView(APIView):
    def post(self, request):
        merchant_id = request.data.get('MerchantID')
        amount = request.data.get('Amount')
        callback_url = request.data.get('CallbackURL')
        description = request.data.get('Description')

        merchant_errors = validators.validate_merchant_id(merchant_id)
        if merchant_errors:
            return helpers.create_response(
                status_code=-9,
                errors={'MerchantID': merchant_errors}
            )

        amount_errors = validators.validate_amount(amount)
        if amount_errors:
            return helpers.create_response(
                status_code=-9,
                errors={'Amount': amount_errors}
            )

        callback_url_errors = validators.validate_callback_url(callback_url)
        if callback_url_errors:
            return helpers.create_response(
                status_code=-9,
                errors={'CallbackURL': callback_url_errors}
            )

        description_errors = validators.validate_description(description)
        if description_errors:
            return helpers.create_response(
                status_code=-9,
                errors={'Description': description_errors}
            )

        try:
            merchant_object = models.Merchant.objects.get(
                merchant_id=merchant_id)
        except models.Merchant.DoesNotExist:
            return helpers.create_response(status_code=-9)

        transaction = models.Transaction.objects.create(
            merchant=merchant_object,
            authority=helpers.generate_authority(),
            amount=amount,
            callback_url=callback_url,
            description=description,
        )

        return helpers.create_response(
            status_code=100,
            authority=transaction.authority
        )
