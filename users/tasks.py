from celery import shared_task
from devs.models import ErrorLog
import traceback
import logging
from utils.mails import sendmail

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
