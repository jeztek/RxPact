import calendar, pytz
from datetime import datetime

def stringToEpochMilli(input, timezone):
    p = pdt.Calendar()
    result, what = p.parse(input)

    if what == 0:
        return None
    
    lt = timezone.localize(datetime(*result[:6]))
    return calendar.timegm(lt.astimezone(pytz.utc).timetuple())*1000

def epochMilliToString(millisec, timezone):
    timestamp = datetime.fromtimestamp(millisec/1000.0, tz=pytz.utc)
    loc_timestamp = timestamp.astimezone(timezone)
    return loc_timestamp.strftime('%x %X%z (%Z)')
