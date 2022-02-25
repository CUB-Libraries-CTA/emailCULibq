from celery.task import task
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os, jinja2
from jinja2 import Environment, PackageLoader
username= os.getenv('EMAIL_HOST_USER')
password= os.getenv('EMAIL_HOST_PASSWORD')
smtp_host= os.getenv('EMAIL_SMTP_HOST')

@task()
def sendEmail(receiver_email,sender_email,subject,template="default_template.html.j2",template_data={"name":"CU Libraries"},verified_email='libnotify@colorado.edu'):
    """
    CU Libraries email task.
    args: receiver_email,sender_email,subject
    kwargs: template,template_data
    Example Submission: See Readme
    """
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = verified_email
    message["To"] = receiver_email
    message["CC"] = sender_email
    env = Environment(loader=PackageLoader('emailCULibq', 'tasks/templates'))
    if template:
        email_template = env.get_template(template)
        text = email_template.render(template_data)
        part1 = MIMEText(text, template.split('.')[-2])
    else:
        raise Exception("Error has occured. Template was not found!")

    message.attach(part1)
    
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    rcpt= [sender_email] + receiver_email.split(',')
    with smtplib.SMTP(smtp_host, 587) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(username, password)
        server.sendmail(
            verified_email, rcpt, message.as_string()
        )