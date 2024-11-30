from . import models


def validate_merchant_id(merchant_id):
    """
    Validates the MerchantID field.
    """
    errors = []

    if not merchant_id:
        errors.append("The merchant id field is required.")
    elif len(merchant_id) < 36:
        errors.append("The merchant id must be at least 36 characters.")
    elif len(merchant_id) > 36:
        errors.append(
            "The merchant id must not be greater than 36 characters.")
    elif not is_valid_merchant_id(merchant_id):
        errors.append("The selected merchant id is invalid.")

    return errors


def is_valid_merchant_id(merchant_id):
    """
    Checks if the provided MerchantID exists in the database.
    """
    try:
        models.Merchant.objects.get(merchant_id=merchant_id)
        return True
    except models.Merchant.DoesNotExist:
        return False


def validate_amount(amount):
    """
    Validates the Amount field.
    """
    errors = []

    if not amount:
        errors.append("The amount field is required.")
    elif amount < 1000:
        errors.append("The amount must be at least 1000.")

    return errors


def validate_callback_url(callback_url):
    """
    Validates the CallbackURL field.
    """
    errors = []

    if not callback_url:
        errors.append("The callback url field is required.")

    return errors


def validate_description(description):
    """
    Validates the Description field.
    """
    errors = []

    if not description:
        errors.append("The description field is required.")

    return errors


def validate_authority(authority, merchant):
    """
    Validates the Authority field. This validator is used with the PaymentVerification process.
    """
    errors = []
    flag = False  # An invalid authority always returns the same error message.

    try:
        transaction = models.Transaction.objects.get(authority=authority)
        if transaction.merchant.merchant_id != merchant:
            flag = True
    except models.Transaction.DoesNotExist:
        flag = True

    if flag:
        errors.extend(
            [
                'Session is not this merchant_id session.',
                '-53',
            ]
        )

    return errors
