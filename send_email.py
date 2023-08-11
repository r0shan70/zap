import boto3
from botocore.exceptions import NoCredentialsError
import os
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import zipfile

# Set your AWS credentials
aws_access_key = 'AKIAQ5OENXUUTLYD4Z5K'
aws_secret_key = 'yQpxkeHicwUbKIY/ZFEyNUAKZVtfxU+7iV/xwqLh'
region = 'eu-north-1'  # Change to your desired AWS region

# Set email parameters
sender_email = 'roshanofficial27@gmail.com'
recipient_email = 'devopstesting539@gmail.com'
subject = 'Test email with attachment'
body_text = 'This is a test email with attachments sent from boto3.'
body_html = '<html><body><h1>This is a test email with attachments sent from boto3.</h1></body></html>'

# Path to the zip file containing the files you want to attach
zip_file_path = '/home/runner/work/zap/zap/zap_report.zip'

# Connect to Amazon SES
ses = boto3.client('ses', region_name=region, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

# Create a MIME Multipart message
msg = MIMEMultipart('mixed')
msg['Subject'] = subject
msg['From'] = sender_email
msg['To'] = recipient_email

# Attach the text part
msg.attach(MIMEText(body_text, 'plain'))
msg.attach(MIMEText(body_html, 'html'))

# Read the contents of the zip file and attach each file
try:
    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        for file_name in zip_file.namelist():
            with zip_file.open(file_name) as attachment_file:
                attachment_content = attachment_file.read()
                attachment_mime = MIMEApplication(attachment_content)
                attachment_mime.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_name))
                msg.attach(attachment_mime)
except FileNotFoundError:
    print(f"Zip file not found: {zip_file_path}")
except Exception as e:
    print("An error occurred:", str(e))

# Convert the message to a string
raw_message = msg.as_string()

# Send the email with attachments
try:
    response = ses.send_raw_email(
        Source=sender_email,
        Destinations=[recipient_email],
        RawMessage={'Data': raw_message}
    )
    print("Email with attachments sent successfully!")
except NoCredentialsError:
    print("AWS credentials not found, or incorrect.")
except Exception as e:
    print("An error occurred:", str(e))
