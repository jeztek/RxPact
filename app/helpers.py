import calendar, pytz
from datetime import datetime

from twilio.rest import TwilioRestClient

from settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_SMS_NUMBER
 
def datetimeToEpochMilli(input, timezone):
    lt = timezone.localize(input)
    return calendar.timegm(lt.astimezone(pytz.utc).timetuple())*1000

def epochMilliToString(millisec, timezone):
    timestamp = datetime.fromtimestamp(millisec/1000.0, tz=pytz.utc)
    loc_timestamp = timestamp.astimezone(timezone)
    return loc_timestamp.strftime('%x %X%z (%Z)')

def send_sms(to, msg):
    client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    sms = client.sms.messages.create(to=to, from_=TWILIO_SMS_NUMBER,
                                     body=msg[:159])

