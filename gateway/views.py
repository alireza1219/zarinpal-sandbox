from datetime import timedelta
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from api import models


def sandbox_payment_view(request, authority):
    try:
        transaction = models.Transaction.objects.get(authority=authority)
    except models.Transaction.DoesNotExist:
        return render(request, "error.html", {"message": "The authority is not valid."}, status=404)

    if now() > transaction.created_at + timedelta(minutes=30):
        return render(request, "error.html", {"message": "The transaction has expired."}, status=400)

    return render(request, "gateway.html", {"transaction": transaction})


@csrf_protect
@require_http_methods(["POST"])
def sandbox_payment_process_view(request):
    authority = request.POST.get('authority')
    payment_status = request.POST.get('payment_status')

    try:
        transaction = models.Transaction.objects.get(authority=authority)
    except models.Transaction.DoesNotExist:
        return render(request, "error.html", {"message": "The authority is not valid."}, status=404)

    if now() > transaction.created_at + timedelta(minutes=30):
        return render(request, "error.html", {"message": "The transaction has expired."}, status=400)

    if payment_status == 'success':
        transaction.status = models.Transaction.SUCCESS
    else:
        transaction.status = models.Transaction.FAILED

    transaction.save()

    return redirect(transaction.callback_url)
