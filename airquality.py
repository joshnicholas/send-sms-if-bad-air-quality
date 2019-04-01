import feedparser
import time
import csv
import datetime
from twilio.rest import Client

account_sid = "TWILIO SID"
auth_token = "TWILIO AUTH TOKEN"
client = Client(account_sid, auth_token)

hours = 0
have_messaged = False

while True:
    now = datetime.datetime.now()
    feed = feedparser.parse('http://dosairnowdata.org/dos/RSS/Colombo/Colombo-PM2.5.xml') #INSERT AQ RSS FEED FOR YOUR CITY
    feed_list = feed['entries'][-1]['summary'].split(';')
    air_quality = feed_list[3]
    ffs = [now, air_quality]
    with open('/airquality.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(ffs)
    hours += 1
    if int(air_quality) >= 101 and have_messaged == False:
        message = client.messages \
                        .create(
                                from_ = 'FROM NUMBER',
                                body = f"""Hey, the air quality reading in CITY is currently{air_quality}. This is unhealthy. Duck for cover!""",
                                to = 'TO NUMBER',
                                status_callback = 'CALLBACK URL',
                                )
        have_messaged = True
    if hours == 24:
        hours = 0
        have_messaged = False
    time.sleep(3600)
