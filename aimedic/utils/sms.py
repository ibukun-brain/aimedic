import random

from sinum.utils.settings import get_app_settings, get_env_variable
from twilio.rest import Client


def generate_verification_code(n=6):
    """generate rando digits of length `n`"""
    num = ""
    for _ in range(n):
        num += str(random.randint(0, 10))

    return num


def send_sms(to, body):
    """
    sends twilio sms to specified number using the `to` argument
    and the content of the message using the `body` argument
    """
    if "prod" in get_app_settings():
        # Your Account SID from twilio.com/console
        account_sid = get_env_variable("TWILLO_ACCOUNT_SID", "xxxx")
        auth_token = get_env_variable("TWILLO_AUTH_TOKEN", "xxxx")
        from_number = get_env_variable("TWILLO_NUMBER", "xxxx")

        client = Client(account_sid, auth_token)

        message = client.messages.create(to=to, from_=from_number, body=body)
        print(message.sid)
    else:
        template = f""""
            ==== BODY =====
            {body}
            ===============
            """
        print(template)
