# importing the requests library
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from datetime import datetime, timedelta;
import json;

from json2html import json2html

# User input parameters
PINCODE = '<User Input>'
nextupcomingDays = 10
gmail_user = '<User Input>'
gmail_password = '<User Input>'
fromAddr = '<User Input>'
toAddr = '<User Input>'
timeIntervalInSeconds=10


def sendNotificationEmail(emilText):
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Vaccination slot notification"
        msg['From'] = fromAddr
        msg['To'] = toAddr
        part1 = MIMEText("subject", 'plain')
        part2 = MIMEText(json2html.convert(emilText), 'html')
        msg.attach(part1)
        msg.attach(part2)
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(gmail_user, gmail_password)
        text = msg.as_string()
        smtpObj.sendmail(fromAddr, toAddr, text)
        smtpObj.quit()
        print
        'Email sent!'
    except Exception as e:
        print
        'Something went wrong...'


def getVaccineAvailabiliySlot():
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin"
    DATE = getSlotForUpcomingDays();
    PARAMS = {'pincode': PINCODE, 'date': DATE}
    r = requests.get(URL, PARAMS)
    data = r.json();
    json_object = json.loads(str(data).replace("'", "\""))
    sendNotificationEmail(json_object)
    return data


def getSlotForUpcomingDays():
    dates = [];
    today = datetime.today()
    for i in range(1, nextupcomingDays):
        today = today + timedelta(1);
        formattedDate = today.strftime("%d-%m-%Y")
        dates.append(formattedDate)
    return formattedDate


if __name__ == "__main__":

    while True:
        getVaccineAvailabiliySlot()
        time.sleep(timeIntervalInSeconds)
