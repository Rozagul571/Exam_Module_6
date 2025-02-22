import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(receiver_email, code):
    sender_email = "nodirbekovarozagul@gmail.com"
    password = "vvbqnhjruknpepal"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Verify Code"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"Verification Code: {code}"
    part = MIMEText(text, "plain")
    message.attach(part)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        print(f"Email yuborishda xatolik: {e}")