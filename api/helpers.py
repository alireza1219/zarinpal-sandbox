import uuid
from rest_framework.response import Response
from rest_framework import status as http_status


def generate_authority():
    """
    Generates a random 36 character authority.
    """
    return f"A{'0' * 20}{uuid.uuid4().hex[:15]}"


def create_response(status_code, errors=None, authority='', http_status_code=http_status.HTTP_200_OK):
    """
    Creates a standardized response for the API.
    """
    response_data = {
        "Status": status_code,
    }

    if errors:
        response_data["errors"] = errors

    if authority:
        response_data["Authority"] = authority

    return Response(response_data, status=http_status_code)
