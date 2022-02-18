import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
context = ssl.create_default_context()
smtp_port = 465
smtp_username = ""
smtp_password = ""

def sendmail(suppliedMSG,qSendLog,suppliedSUB=None):
    msg = MIMEMultipart()
    msg["From"] = "Lutetium <lutium@jamesdev.co.gg>"
    msg["To"] = ""
    if suppliedSUB is None:
        msg["Subject"] = "Lutetium"
    else:
        msg["Subject"] = f"Lutetium - {suppliedSUB}"
    msg.attach(MIMEText(suppliedMSG))
    if qSendLog:
        with open("/home/pi/Lutetium/LUcron.log", "rb") as attachment:
            p = MIMEApplication(attachment.read(), _subtype="log")
            p.add_header('Content-Disposition', "attachment; filename= %s" % "LUcron.log")
            msg.attach(p)

    with smtplib.SMTP_SSL("", smtp_port, context=context) as server:
        server.login(smtp_username, smtp_password)
        server.sendmail(msg["From"], msg["To"], msg.as_string())
