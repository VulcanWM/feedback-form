import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import ssl
from flask import session

def send_mail(title, email, description):  
    context = ssl.create_default_context()
    MAILPASS = os.getenv("MAIL_PASSWORD")
    MAIL = os.getenv("MAIL")
    html = f"""
    <h1>{title}</h1>
    <p>{description}</p>
    <p>From {email}</p>
    """
    message = MIMEMultipart("alternative")
    message["Subject"] = "Feedback Form"
    part2 = MIMEText(html, "html")
    message.attach(part2)
    try:
      sendermail = MAIL
      password = MAILPASS
      gmail_server = smtplib.SMTP('smtp.gmail.com', 587)
      gmail_server.starttls(context=context)
      gmail_server.login(sendermail, password)
      message["From"] = sendermail
      message["To"] = sendermail
      gmail_server.sendmail(sendermail, sendermail, message.as_string())
      return True
    except:
      return "Verification email not sent, due to some issues."
      gmail_server.quit()

def addcookie(key, value):
  session[key] = value

def delcookies():
  session.clear()

def getcookie(key):
  try:
    if (x := session.get(key)):
      return x
    else:
      return False
  except:
    return False