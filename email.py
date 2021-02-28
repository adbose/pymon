import email_credentials
import smtplib


def send_alert_email(msg):
    sender_address = email_credentials.email_id
    receiver_address = "adi26mar@gmail.com"
    account_password = email_credentials.password
    subject = "Alert"
    body = msg

    # Endpoint for the SMTP Gmail server
    smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
 
    # Login with your Gmail account using SMTP
    smtp_server.login(sender_address, account_password)
 
    message = f"Subject: {subject}\n\n{body}"
    smtp_server.sendmail(sender_address, receiver_address, message)
 
    # Close our endpoint
    smtp_server.close()
