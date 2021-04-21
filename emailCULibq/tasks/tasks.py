from celery.task import task
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os, jinja2
from jinja2 import Environment, PackageLoader
username= os.getenv('EMAIL_HOST_USER')
password= os.getenv('EMAIL_HOST_PASSWORD')

@task()
def sendEmail(sender_email,receiver_email,subject,template=None,template_data=None):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    env = Environment(loader=PackageLoader('emailCULibq', 'tasks/templates'))
    # template = env.get_template('index.html')
    # templateLoader = jinja2.FileSystemLoader(searchpath="./templates/")
    # templateEnv = jinja2.Environment(loader=templateLoader)
    if template:
        email_template = env.get_template(template)
        # email_template = templateEnv.get_template("/usr/local/lib/python3.6/site-packages/emailCULibq/tasks/templates/{0}".format(template))
        text = email_template.render(template_data)
        part1 = MIMEText(text, template.split('.')[-2])
    else:
        text="Error has occured. Template was not found!"
        part1 = MIMEText(text, "plain")
    message.attach(part1)
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.colorado.edu", 587, context=context) as server:
        server.login(username, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )