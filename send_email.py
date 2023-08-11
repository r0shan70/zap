import boto3
from botocore.exceptions import NoCredentialsError
import os
import zipfile
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Set your AWS credentials
aws_access_key = 'AKIAQ5OENXUUTLYD4Z5K'
aws_secret_key = 'yQpxkeHicwUbKIY/ZFEyNUAKZVtfxU+7iV/xwqLh'
region = 'eu-north-1'  # Change to your desired AWS region

# Set email parameters
sender_email = 'roshanofficial27@gmail.com'
recipient_email = 'devopstesting539@gmail.com'
subject = 'Test email with attachments'
body_text = 'This is a test email with an attached zip file sent from boto3.'
body_html = '<html><body><h1>This is a test email with an attached zip file sent from boto3.</h1></body></html>'

# Path to the folder containing the files you want to zip and attach
source_folder_path = '/home/runner/work/zap/zap/'  # Update this to your folder path

# Path to save the generated zip file
zip_file_path = '/home/runner/work/zap/zap/zap_report.zip'  # Update this to the desired zip file path

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

# Create a zip file containing all files in the source folder
with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(source_folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, os.path.relpath(file_path, source_folder_path))

# Read the content of the zip file
with open(zip_file_path, 'rb') as attachment_file:
    attachment_content = attachment_file.read()

# Attach the zip file
attachment_mime = MIMEApplication(attachment_content)
attachment_mime.add_header('Content-Disposition', 'attachment', filename=os.path.basename(zip_file_path))
msg.attach(attachment_mime)

# Convert the message to a string
raw_message = msg.as_string()

# Send the email with the attached zip file
try:
    response = ses.send_raw_email(
        Source=sender_email,
        Destinations=[recipient_email],
        RawMessage={'Data': raw_message}
    )
    print("Email with attached zip file sent successfully!")
except NoCredentialsError:
    print("AWS credentials not found, or incorrect.")
except Exception as e:
    print("An error occurred:", str(e))
