import yagmail
import os

def send_email(to_list, subject, body):
    email_user = os.environ.get("EMAIL_USER")
    email_pass = os.environ.get("EMAIL_PASS")

    yag = yagmail.SMTP(user=email_user, password=email_pass)
    yag.send(to=to_list, subject=subject, contents=body)
