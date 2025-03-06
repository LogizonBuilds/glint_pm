import logging
import traceback
import uuid
from django.core.mail import EmailMessage, send_mail
from django.template import Context
from django.template.loader import get_template, render_to_string
from devs.models import ErrorLog
import random
import string

logger = logging.getLogger(__name__)


def sendmail(
    subject: str,
    message: str,
    user_email: str,
    username: str = "Participants",
    from_email: str = "hello@glintpm.com",
    other_email=None,
    template_name="verification_email.html",
) -> None:
    """
    This function sends an email to the specified user.

    Args:
        subject (str): The subject of the email.
        message (str): The message body of the email.
        user_email (str): The email address of the user.
        username (str): The username of the user.
        from_email (str, optional): The email address of the sender. Defaults to 'truebone002@gmail.com'.

    Returns:
        None: This function does not return a value.

    Raises:
        Exception: If there is an error sending the email, an exception is raised.
    """
    ctx = {"message": message, "subject": subject, "username": username}

    # Use render_to_string to render the template and get the HTML content
    html_content = get_template(template_name).render(ctx)

    if not other_email:
        msg = EmailMessage(
            subject,
            html_content,
            from_email,
            [user_email],
        )
    else:
        msg = EmailMessage(
            subject,
            html_content,
            from_email,
            [user_email, other_email],
        )

    msg.content_subtype = "html"

    msg.extra_headers["Reply-To"] = "hello@glintpm.com"
    # msg.send()

    try:
        msg.send()
    except Exception as e:
        stack_trace = traceback.format_exc()
        ErrorLog.objects.create(
            error=f"Error sending email to {user_email}",
            traceback=stack_trace,
            app_name="send_mail",
            severity="ERROR",
        )
        logger.error(f"Error sending email to {user_email} due to {e}")
        traceback.print_exc()
        pass
