import os
from os.path import join, dirname
from dotenv import load_dotenv  # noqa
from pushover import init, Client  # noqa
from datetime import datetime
from datetime import timedelta
import requests
from icalendar import Calendar, Event, vDatetime
from pytz import timezone

# load .env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# start pushover
usertoken = os.getenv('USERTOKEN')
token = os.getenv('TOKEN')
init(token)

tz = timezone('Europe/London')

calendar = os.getenv('CALENDAR')

# scan todays events
date = (datetime.now() + timedelta(days=0))
datefor = "%s" % date.strftime('%Y-%m-%d')

r = requests.get(calendar)
gcal = Calendar.from_ical(r.text)

for event in gcal.walk('VEVENT'):
    # Get starting time
    if 'DTSTART' in event:
        try:
            dtstart = event['DTSTART'].dt.astimezone(timezone('Europe/London'))
        except event.DoesNotExist:
            dtstart = False

    # Get ending time
    if 'DTEND' in event:
        try:
            dtend = event['DTEND'].dt.astimezone(timezone('Europe/London'))
        except event.DoesNotExist:
            dtend = False

    # Print event info
    if dtstart or dtend:
        if datefor in "%s" % dtstart or datefor in "%s" % dtend:
            message1 = event['summary']

            if dtstart and dtend:
                length = (dtend - dtstart).total_seconds() / 60
            else:
                length = False

            if length:
                message2 = "Start: %s for %s minutes" % (dtstart, length)
                print(message1, message2)
                Client(usertoken).send_message(message2, title=message1)
                print('Notification sent')
