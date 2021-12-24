import os
from erp.marketing.campaign.sms import SendSMS
from erp.marketing.campaign.Mail import SendMail
from plyer import notification

sender = SendSMS()
email_sender = SendMail()


def create_notification(title="Harlos-ERP", message="New notification", timeout=7200):
    try:
        base_path = os.getcwd()
        linux_logo_path = "erp/static/img/logo.png"
        window_logo_path = "erp/static/img/logo.ico"
        image_path = os.path.join(base_path, linux_logo_path)
        # print(image_path, title, message)

        notification.notify(
            title=title, message=message, timeout=timeout, app_icon=image_path
        )
        print("Notification made")
    except Exception as bug:
        print(bug)
        try:
            image_path = os.path.join(base_path, window_logo_path)
            notification.notify(
                title=title, message=message, timeout=timeout, app_icon=image_path
            )
        except Exception as bug:
            print(bug)
            print("Failed making notification")
            return False


def create_sms_notification(title: str, message: str, phone: str = "0718235915"):
    try:
        if message and phone:
            message = f"{title}\n\n{message}"
        sender.send_sms(message, phone)
        print("Notification have been made !!")
    except Exception as bug:
        print(bug)
        print("Failed to create a SMS Notification")


def create_email_notification(
    message: str, email: str = "sales@harloscontainers.com"
) -> bool:
    try:
        if message and email:
            email_sender.send_mail(message, email)
        print("Email notification Made")
    except Exception as bug:
        print(bug)
        print("Exception raised while creating email notification")
        return False


def make_notification(title: str, message: str):
    """make_notification [summary]

    Args:
        title (str): [description]
        message (str): [description]
    """
    create_notification(title, message)
    create_sms_notification(title, message)
    create_email_notification(message=message)