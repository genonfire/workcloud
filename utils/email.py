from smtplib import SMTPException

from django.conf import settings
from django.core.mail import (
    BadHeaderError,
    EmailMultiAlternatives,
    get_connection
)
from django.template.loader import render_to_string

from core.wrapper import async_func
from utils.debug import Debug


class _EmailHelper(object):
    def _recipient_list(self, recipients):
        if isinstance(recipients, list):
            return recipients

        data = []
        for index, recipient in enumerate(recipients.split(',')):
            data.append(recipient.strip())
        return data

    @async_func
    def _send(
        self, subject, body, from_email=None, to=None, bcc=None, cc=None,
        html_subject=None, html_body=None, attachment=None, filename=None,
        mimetype=None, context=None
    ):
        if settings.DO_NOT_SEND_EMAIL:
            return
        if not from_email:
            from_email = settings.DEFAULT_FROM_EMAIL

        if html_subject:
            subject = render_to_string(html_subject, context)
        subject = ''.join(subject.splitlines())

        email = EmailMultiAlternatives(
            subject=subject,
            body=body,
            from_email=from_email,
            to=to,
            bcc=bcc,
            cc=cc
        )
        if html_body:
            html_email = render_to_string(html_body, context)
            email.attach_alternative(html_email, 'text/html')
        if attachment and filename and mimetype:
            email.attach(filename, attachment, mimetype)

        try:
            email.send(fail_silently=False)
        except BadHeaderError:
            Debug.error("BadHeaderError")
        except SMTPException:
            Debug.error("SMTPException")

    def send_to(
        self, subject, body, from_email=None, user=None, email=None,
        html_subject=None, html_body=None, attachment=None, filename=None,
        mimetype=None, context=None
    ):
        """
        Send a single email to a single user or email

        to send html subject, pass return of render_to_string
        """
        if not user and not email:
            raise AssertionError("Either user or email should be presented.")
        elif not email:
            email = user.email
        Debug.trace(" Sending mail to %s" % email)

        self._send(
            subject=subject,
            body=body,
            from_email=from_email,
            to=[email],
            html_subject=html_subject,
            html_body=html_body,
            attachment=attachment,
            filename=filename,
            mimetype=mimetype,
            context=context
        )

    def send_bcc(
        self, subject, body, from_email=None, to=None, recipients=None,
        html_subject=None, html_body=None, attachment=None, filename=None,
        mimetype=None, context=None
    ):
        """
        Send a single email to single or multiple recipient as cc

        to send html subject, pass return of render_to_string
        """
        bcc = self._recipient_list(recipients)
        Debug.trace(" Sending mail to %d bcc" % len(bcc))

        self._send(
            subject=subject,
            body=body,
            from_email=from_email,
            to=[to],
            bcc=bcc,
            html_subject=html_subject,
            html_body=html_body,
            attachment=attachment,
            filename=filename,
            mimetype=mimetype,
            context=context
        )

    @async_func
    def send_mass(self, messages):
        """
        Send multiple emails at once

        messages are list of EmailMultiAlternatives
        """
        if settings.DO_NOT_SEND_EMAIL:
            return
        connection = get_connection(fail_silently=False)
        Debug.trace(" Sending %d mass messages" % len(messages))
        connection.send_messages(messages)
        Debug.trace(" Sending mass messages completed.")


EmailHelper = _EmailHelper()
