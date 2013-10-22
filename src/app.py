from flask import request
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from subprocess import Popen, PIPE
from email.mime.text import MIMEText
import smtplib
from auth import requires_auth

app = Flask(__name__)      

EMAIL_TO = 'foo@bar.com'
EMAIL_FROM = 'baz@bar.com'
EMAIL_LOGIN_USERNAME = 'joe@bar.com'
EMAIL_LOGIN_PASSWORD = '1234'

SCRIPT_PATH = '/path/to/virtualenv/app/bin/update_jekyll.sh'

def send_email(subject, body):
  server = smtplib.SMTP('smtp.gmail.com:587')
  server.starttls()
  server.login(EMAIL_LOGIN_USERNAME, EMAIL_LOGIN_PASSWORD)
  
  msg = MIMEText(body)
  msg['To'] = EMAIL_TO
  msg['From'] = EMAIL_FROM
  msg['Subject'] = subject
  
  server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
  server.quit() 
 
@app.route('/', methods=['POST', ])
@requires_auth
def update_jekyll():
  body = ''
  try:
    if 'commit' in request.form:
        body = request.form.get('commit', 'None')
    (stdout, stderr) = Popen([SCRIPT_PATH,], stdout=PIPE).communicate()
    send_email("Bitbucket post commit hook succesfully executed", "Response: %s" % body)
    return 'Success' 
  except:
    send_email("Error with Bitbucket post commit hook", "There was an error performing the script associated with the post commit hook")  

app.wsgi_app = ProxyFix(app.wsgi_app)
 
if __name__ == '__main__':
  app.run()

