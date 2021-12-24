from flask import current_app as app
from flask_mail import Mail, Message


class SendMail:
    def __init__(self):
        self.mail_box = Mail()
        self.mail_box.init_app(app)

    def send_mail(self, message: str, recipients: list = []):
        try:
            if recipients:
                print("connection made")
                for recipient_email in recipients:
                    print(f"sending to {recipient_email.email}")
                    msg = Message(
                        sender=("Harlos Containers",
                                "noreply@harloscontainers.com"),
                        body=message,
                        subject="Harlos Containers",
                        recipients=[recipient_email.email],
                    )
                    self.mail_box.send(msg)
                    print("message has been sent")
            return False

        except Exception as bug:
            print(bug)
            print("Bug thrown while sending an email")
            return False

    def bulk_mail(self):
        pass
