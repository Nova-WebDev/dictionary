import smtplib
from auth.core.interfaces.email_sender import IEmailSender
from auth.infrastructure.email.email_template import EmailTemplate
from app.settings import settings


class EmailSender(IEmailSender):
    async def send(self, email: str, code: str):
        msg = EmailTemplate.verification_code_template(email, code)
        msg["From"] = settings.sender_email
        msg["To"] = email

        with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port) as server:
            server.login(settings.sender_email, settings.app_password)
            server.send_message(msg)
