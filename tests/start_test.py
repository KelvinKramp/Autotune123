import subprocess
from tests.mailgun import send_message_mailgun
import json
import os
from datetime import datetime as dt
import datetime
from definitions import development, ROOT_DIR


# RUN TESTING UNIT
test_file_path = os.path.join(ROOT_DIR, "tests", "testing.py")
subprocess.run("python "+test_file_path+" 2> unittest_log.txt", shell=True)

# SET VARIABLES FOR MAIL
if development:
    secrets_path = os.path.join(ROOT_DIR, "tests", "secrets.json")
    with open(secrets_path) as f:
        secret = json.load(f)
    developer = secret["developer"]
    sender = secret["sender"]
    smtp_login = secret["smtp_login"]
    password = secret["password"]
    smtp_server = secret["MAILGUN_SMTP_SERVER"]
    port = secret["MAILGUN_SMTP_PORT"]
else:
    developer = os.environ["developer"]
    smtp_login = os.environ["MAILGUN_SMTP_LOGIN"]
    smtp_server = os.environ["MAILGUN_SMTP_SERVER"]
    port = int(os.environ["MAILGUN_SMTP_PORT"])
    sender = "you@" + str(os.environ["MAILGUN_DOMAIN"])
    password = os.environ["MAILGUN_SMTP_PASSWORD"]



# DEFINE TEXT FOR MAIL
attachment_file = os.path.join(ROOT_DIR, "tests", "unittest_log.txt")
with open(attachment_file, 'r') as f:
    log_file_text = f.read()
if "OK" in str(log_file_text):
    status = "OK"
else:
    status = "ERROR"
date = ((str(dt.now(datetime.timezone.utc).day)+"-"+str(dt.now(datetime.timezone.utc).month)+"-"+str(dt.now(datetime.timezone.utc).year)))
text = log_file_text
subject = "Unittest result " + date + ":" + status

# SEND MAIL
send_message_mailgun(text, subject, developer, sender, smtp_login, password, smtp_server, port)

