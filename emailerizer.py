# emailerizer.py
"""Sends personalized email to multiple contacts via Gmail.
"""

import email, smtplib, ssl, csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# modules below needed if sending attachments
# from email import encoders
# from email.mime.base import MIMEBase

#! ENTER YOUR CUSTOM INFO IN THE 3 LINES BELOW:
sender_email = "YOUR_EMAIL_ADDRESS_GOES_HERE"
password = "YOUR_PASSWORD_GOES_HERE" # Gmail app password
subject = "SUBJECT_OF_YOUR_EMAIL_GOES_HERE"

# Extract first name and email from .csv and put them into a dictionary
client_dict = {}
with open('contacts.csv', 'r', newline='') as client_contacts:
    reader = csv.reader(client_contacts)
    for contact in reader:
        name, email = contact
        client_dict.update({name: email})

# Extract text for body of email from .txt file
email_body = ''
with open('email_body.txt', 'r') as message:
    email_body = message.read()

for receiver_name, receiver_email in client_dict.items():
    # Combining strings to personalize email
    body = f'Hello {receiver_name}' + email_body
    
    # Creating the multipart message and setting the headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
#    message["Bcc"] = receiver_email  # Use only if BCC needed (and comment out line above)
    message["Subject"] = subject
    # Add body to email
    message.attach(MIMEText(body, "plain"))   
    text = message.as_string()

    # Logging in to server using secure context. Then sending the email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)