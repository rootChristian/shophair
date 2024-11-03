'''
************************************************************************
*************** Author:   Christian KEMGANG NGUESSOP *******************
*************** Project:   shophair                  *******************
*************** Version:  1.0.0                      *******************
************************************************************************
'''

import random
from django.core.mail import EmailMessage
from .models import OneTimePassword, User
from shophair.settings import base

def generateOtp():
    otp = ""

    for i in range (6):
        otp += str(random.randint(1, 9))
    return otp

def sendNormalEmail(data):
    email=EmailMessage(
        subject=data["email_subject"],
        body=data["email_body"],
        from_email=base.EMAIL_HOST_USER,
        to=[data["to_email"]]
    )
    email.send()

def sendOtpCodeToEmail(email):
    subject = "One time passcode for email verification"
    # Generate the otp
    otp = generateOtp()
    current_site = "http://localhost:8000/api/v1/auth/verify-email/" #"shophair.com"
    user = User.objects.get(email=email)
    email_body = (
        f"Hi {user.first_name},\n\n"
        f"thanks for signing up on {current_site}\n"
        f"Please verify your email with the one time passcode (OTP):  {otp}\n\n"
        f"Best regards,\n"
        f"Shophair Company"
    )
    from_email = base.EMAIL_HOST_USER
    # Save the otp on database 
    otp_obj = OneTimePassword.objects.create(user=user, otp=otp)
    # Send the email 
    email_message = EmailMessage(subject=subject, body=email_body, from_email=from_email, to=[user.email])
    email_message.send(fail_silently=True)
    