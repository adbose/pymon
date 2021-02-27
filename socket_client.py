import socket
import psutil
import json
import smtplib
import time
import email_credentials



client_socket = socket.socket()
host = '127.0.0.1'
port = 1233

print('Waiting for connection...')


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


try:
    client_socket.connect((host, port))
except socket.error as e:
    error_message  = str(e)
    print(error_message)
    send_alert_email(error_message)

response = client_socket.recv(1024)

while True:
    print('Client device running...')
    # device status
    device_status = 1  # 1 is assigned to show device is running
    # cpu utilization
    cpu_usage = psutil.cpu_percent(1)
    
    if cpu_usage >= 80.0:
        send_alert_email(cpu_usage)

    memory_usage = psutil.virtual_memory()
    data = {
        "status": 1,
        "cpu": cpu_usage,
        "memory": memory_usage    
    }
    data_str = json.dumps(data)
    client_socket.send(str.encode(data_str))
    response = client_socket.recv(1024)
    time.sleep(5)  
    print(response.decode('utf-8'))


client_socket.close()