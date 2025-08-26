from email.message import EmailMessage
import smtplib
import os

def send_email_with_attachment(to_address, subject, body, attachment_path):
    msg = EmailMessage()
    msg['From'] = os.getenv('EMAIL_USER')
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.set_content(body)

    with open(attachment_path, 'rb') as attachment:
        msg.add_attachment(attachment.read(), maintype='application', subtype='pdf', filename=os.path.basename(attachment_path))

    try:
        with smtplib.SMTP(os.getenv('SMTP_SERVER'), os.getenv('SMTP_PORT')) as server:
            server.starttls()
            server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
            server.send_message(msg)
        return True, "Email sent successfully."
    except Exception as e:
        return False, str(e)