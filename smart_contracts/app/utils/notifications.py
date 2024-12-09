from flask_mail import Mail, Message

mail = Mail()

def send_notification(to_email, subject, body):
    msg = Message(subject, recipients=[to_email], body=body)
    mail.send(msg)
