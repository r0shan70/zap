import boto3
from botocore.exceptions import NoCredentialsError
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import shutil
import json

# Read AWS credentials from the file
with open('aws_credentials.json') as f:
    aws_credentials = json.load(f)

 

aws_access_key = aws_credentials.get('aws_access_key_id')
aws_secret_key = aws_credentials.get('aws_secret_access_key')

 

# Set your AWS region
region = 'eu-north-1'  # Change to your desired AWS region

# Set email parameters
sender_email = 'roshanofficial27@gmail.com'
recipient_email = 'devopstesting539@gmail.com'
cc_emails = ['hellofabin@gmail.com', 'mathewrijo23@gmail.com']  # Add more CC recipients as needed
subject = 'Test email with attachment'
body_text = 'This is a test email with an attachment sent from boto3.'
body_html = '<html><body><h1>This is a test email with an attachment sent from boto3.</h1></body></html>'

# Path to the file you want to attach
attachment_file_path = 'file.html'

# Connect to Amazon SES
ses = boto3.client('ses', region_name=region, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

# Read the content of the attachment file
with open(attachment_file_path, 'rb') as attachment_file:
    attachment_content = attachment_file.read()

# Create a MIME Multipart message
msg = MIMEMultipart('mixed')
msg['Subject'] = subject
msg['From'] = sender_email
msg['To'] = recipient_email
msg['Cc'] = ', '.join(cc_emails)  # Adding CC recipients

# Attach the text part
msg.attach(MIMEText(body_text, 'plain'))
msg.attach(MIMEText(body_html, 'html'))

# Attach the file
attachment_mime = MIMEApplication(attachment_content, _subtype='html')
attachment_mime.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_file_path))
msg.attach(attachment_mime)

# Convert the message to a string
raw_message = msg.as_string()

# Send the email with attachment
try:
    response = ses.send_raw_email(
        Source=sender_email,
        Destinations=[recipient_email] + cc_emails,
        RawMessage={'Data': raw_message}
    )
    print("Email with attachment sent successfully!")
except NoCredentialsError:
    print("AWS credentials not found, or incorrect.")
except Exception as e:
    print("An error occurred:", str(e))
