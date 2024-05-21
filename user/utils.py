from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from django.core.exceptions import ValidationError
from .models import UserModel


def send_reset_mail(recipient):
    message = MIMEMultipart()
    message["From"] = settings.SMTP_USERNAME
    message["To"] = recipient.email
    message["Subject"] = "Password Reset Request"
    
    uidb64, token = generate_reset_token(recipient)
    
    with open("user/templates/reset_email_message.html", "r") as file:
        body = file.read()
        
    body = body.replace("%%SERVER_NAME%%", settings.SERVER_NAME)
    body = body.replace("%%UIDB64%%", uidb64)
    body = body.replace("%%TOKEN%%", token)
    
    message.attach(MIMEText(body, "html"))
    
    try:
        server = smtplib.SMTP(settings.SMTP_SERVER, settings.EMAIL_PORT)
        server.starttls()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.send_message(message)
        server.quit()
    
    except (smtplib.SMTPConnectError, smtplib.SMTPAuthenticationError, smtplib.SMTPResponseException):
        raise ValidationError("Failed to send email. Please try again.")

    
def generate_reset_token(user):
    generator = PasswordResetTokenGenerator()
    uidb64 = urlsafe_base64_encode(force_bytes(user.id))
    token = generator.make_token(user)
    
    return uidb64, token


class DecodeResetToken():
    def __init__(self, uidb64, token):
        self.uidb64 = uidb64
        self.token = token
        
    def token_check(self):
        generator = PasswordResetTokenGenerator()
        user = self.get_user()
        
        return generator.check_token(user, self.token)
    
    def get_user(self):
        user_id = force_str(urlsafe_base64_decode(self.uidb64))
        user = UserModel.objects.filter(id=user_id).first()
        
        return user