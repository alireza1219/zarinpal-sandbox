from rest_framework.response import Response
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


class PaymentVerificationView(APIView):
    def post(self, request):
        merchant_id = request.data.get('MerchantID')
        authority = request.data.get('Authority')
        amount = request.data.get('Amount')

        merchant_errors = validators.validate_merchant_id(merchant_id)
        if merchant_errors:
            return helpers.create_response(
                status_code=-9,
                errors={'MerchantID': merchant_errors}
            )

        authority_errors = validators.validate_authority(
            authority, merchant_id
        )
        if authority_errors:
            return helpers.create_response(
                status_code=-9,
                # This also appears within the MerchantID in the real API. Don't change it!
                errors={'MerchantID': authority_errors}
            )

        # FIXME: The original API does not check for min/max amount value when verifying the payment.
        # It only checks for the amount field presence.
        # The validate_amount() function checks for the min/max amount value which can cause a misbehavior on the client side.
        amount_errors = validators.validate_amount(amount)
        if amount_errors:
            return helpers.create_response(
                status_code=-9,
                errors={'Amount': amount_errors}
            )

        # No need to check for transaction object existence. It was performed by the validate_authority() function.
        transaction = models.Transaction.objects.get(authority=authority)

        if transaction.amount != int(amount):
            # Amount mismatch.
            return helpers.create_verification_response(-50)

        if transaction.status != models.Transaction.SUCCESS:
            # Transaction is still pending or has been failed.
            return helpers.create_verification_response(-51)

        if transaction.verified:
            # Transaction was verified before. No reverification need.
            return helpers.create_verification_response(101, int(transaction.reference_id))

        # Mark this transaction as verified, then return a proper response.
        reference_id = helpers.generate_reference_id()
        transaction.reference_id = reference_id
        transaction.verified = True
        transaction.save()

        return helpers.create_verification_response(100, reference_id)
