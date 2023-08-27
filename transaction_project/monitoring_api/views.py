from django.shortcuts import HttpResponse
from django.core.mail import send_mail
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from .models import Transaction
from datetime import timedelta

# Constants
TIER_LIMITS = {
    1: 500,
    2: 1000000,
}

scheduler = BackgroundScheduler(jobstores={'default': DjangoJobStore()})
scheduler.start()

# Schedule the time policy evaluation to process transactions every 30 minutes
@scheduler.scheduled_job('interval', minutes=30)
def scheduled_policy_evaluation():
    unprocessed_transactions = Transaction.objects.filter(processed=False)
    for transaction in unprocessed_transactions:
        process_single_transaction(transaction)

# Process a single transaction in a loop
def process_single_transaction(transaction):
    if policy_evaluation(transaction):
        transaction.processed = True
        transaction.save()
    
# Check if the amount paid matches the amount in the chosen tier number and send an email
def policy_evaluation(transaction):
    if transaction.amount <= TIER_LIMITS[transaction.chosen_tier_number]:
        send_notification_email(transaction.user, transaction.amount, transaction.chosen_tier_number)
        
        
def is_user_flagged(user):
    try:
        transaction = Transaction.objects.get(user=user)
        return transaction.flagged
    except Transaction.DoesNotExist:
        return False

def has_recent_transaction(user):
    recent_transaction = Transaction.objects.filter(user=user, timestamp__gte=timezone.now() - timedelta(minutes=1)).first()
    return recent_transaction is not None


# Sending notification email
def send_notification_email(user, amount, chosen_tier_number):
    subject = f"Transaction Alert for {user}"
    message = f"An amount of {amount} has been paid by {user} in Tier {chosen_tier_number}."
    from_email = 'chukwumaonyedika98@gmail.com'
    recipient_list = ['mikkiemiky@gmail.com']

    send_mail(subject, message, from_email, recipient_list)

@csrf_exempt
def process_transaction(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        amount = float(request.POST.get('amount'))
        chosen_tier_number = int(request.POST.get('chosen_tier'))   # Get the chosen tier which are digits 1 and 2, from the frontend

        # Check if user has been previously flagged
        if is_user_flagged(user):
            return HttpResponse(status=400, content="User is flagged. Transaction not allowed.")

        # Check if the amount paid is greater than the tier limit
        if amount > TIER_LIMITS[chosen_tier_number]:
            return HttpResponse(status=400, content=f"Transaction amount exceeds Tier {chosen_tier_number} limit.")

        # Check if the user has performed more than one transactions within a minute
        if has_recent_transaction(user):
            return HttpResponse(status=400, content="Too many transactions within a minute.")

        # Save the user record
        transaction = Transaction.objects.create(
            user=user,
            amount=amount,
            chosen_tier_number=chosen_tier_number,
        )

        # Send an email when a user is successfully created
        policy_evaluation(transaction)

        return HttpResponse(status=200)

