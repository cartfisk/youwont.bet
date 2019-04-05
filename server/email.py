import smtplib
import ssl
from email.mime.text import MIMEText as text

PORT = 465 # For SSL
SMTP_SERVER = "smtp.gmail.com"
SENDER_EMAIL = "only1lushv@gmail.com"
PASSWORD = "6GAE6P!uqt%ak92"

# Create a secure SSL context

def send_email(to_email, message, from_email=SENDER_EMAIL, password=PASSWORD, smtp_server=SMTP_SERVER, port=PORT):
    # Try to log in to server and send email
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(from_email, password)
            server.sendmail(from_email, to_email, message)
    except Exception as e:
        # Print any error messages to stdout
        print(e)

def send_download_email(to_email, download_code):
    message = text("""\
    THANK YOU FOR BEING PART OF THE LIMITED RELEASE.
    YOUR DOWNLOAD LINK IS BELOW:
    -----------------------------------------------
                vlush - pace yourself
    -----------------------------------------------
    https://youwont.bet/api/v1/download/{}.zip
    -----------------------------------------------

    If you are having trouble getting the link to open,
    copy and paste it into your browser's URL bar.

    PLEASE NOTE: Download codes can only be used ONCE,
    make sure you use a computer to download.
    """.format(download_code))

    message['From'] = SENDER_EMAIL
    message['To'] = to_email
    message['Subject'] = "vlush - pace yourself - limited release"

    send_email(to_email, message.as_string(), SENDER_EMAIL, PASSWORD, SMTP_SERVER, PORT)
