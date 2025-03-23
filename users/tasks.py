from celery import shared_task
from devs.models import ErrorLog
import traceback
import logging
from utils.mails import sendmail
from utils.utils import FlutterSDK
from users.models import Transaction
from constants.constants import TransactionStatus

logger = logging.getLogger(__name__)


@shared_task
def send_email_verification_task(subject, message, username, user_email):
    try:
        sendmail(subject, message, user_email, username)
    except Exception:
        traceback.print_exc()
        ErrorLog.objects.create(
            app_name="send_email_verification_task",
            traceback=traceback.format_exc(),
            severity="ERROR",
        )
        logger.error(traceback.format_exc())


@shared_task
def verify_payment_status_task():
    # get all pending trancactions
    try:
        transactions = Transaction.objects.filter(
            transaction_status=TransactionStatus.PENDING.value
        ).order_by("-transaction_date")
        for transaction in transactions:
            tx_ref = transaction.transaction_reference
            flutter_sdk = FlutterSDK(tx_ref=tx_ref)
            status = flutter_sdk.get_transaction_status()
            print("This is the status: ", status)
            if status == "successful":
                transaction.transaction_status = TransactionStatus.SUCCESS.value
                transaction.save()
            elif status == "failed":
                transaction.transaction_status = TransactionStatus.FAILED.value
                transaction.save()
    except Exception:
        traceback.print_exc()
        ErrorLog.objects.create(
            app_name="verify_payment_status_task",
            traceback=traceback.format_exc(),
            severity="ERROR",
        )
        logger.error(traceback.format_exc())
