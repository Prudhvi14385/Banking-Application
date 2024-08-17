import time
from random import randint
from CPR_Banking.com.service.constants import *


# function that generates random number
def otp_gen():
    otp = randint(100000, 999999)
    return otp


# function that simulates sending mail and verifies OTP
def mailOtpVerification(email):
    # Simulate sending an email by printing the OTP to the console
    otp = otp_gen()
    print(f"Simulated email sent to: {email}")
    print(f"OTP: {otp}")

    user_otp = int(input("Please enter OTP to continue: "))

    if user_otp == otp:
        return True
    else:
        return False
