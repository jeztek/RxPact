import time, pytz
from itertools import chain, groupby
from operator import attrgetter
from datetime import datetime, timedelta

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django import forms
try:
    import json
except:
    import django.utils.simplejson as json
from django.contrib.auth.decorators import login_required

from helpers import datetimeToEpochMilli, send_sms
from account.models import UserNetwork

# Return JSON encoded representation of object as text response
def JsonResponse(obj):
    return HttpResponse(json.dumps(obj, ensure_ascii=False),
                        mimetype="text/plain; charset=\"utf-8\"")

@login_required
def home(request, message=None):

    user_profile = request.user.get_profile()
    timezone = pytz.timezone(user_profile.tz)

    user_meds = request.user.usermedication_set.all()

    # load schedule for each medication and flatten into one list
    user_med_times = list(chain.from_iterable([um.usermedicationschedule_set.all() for um in user_meds]))

    schedule = []
    today = datetime.today()

    # hash by time
    keyfunc = attrgetter('time_scheduled')
    user_med_times = sorted(user_med_times, key=keyfunc)

    for (t, meds) in groupby(user_med_times, keyfunc):
        # Add pretty-printed time and seconds since epoch timestamp
        t = datetime.combine(today, t)
        timestamp = datetimeToEpochMilli(t, timezone)
        hour = t.hour if (t.hour <= 12) else (t.hour-12)
        time = "%d:%s" % (hour, t.strftime("%M %p"))
        schedule.append({
            "time" : time,
            "timestamp" : timestamp,
            "meds" : [m.to_dict() for m in meds],
        })

    user_network = list(UserNetwork.objects.filter(user=request.user).with_colors())[:4]
        
    return render_to_response('app_home.html', {
        'user'      : request.user,
        'user_network' : user_network,
        'message'   : message,
        'schedule'  : schedule,
        'schedule_json' : json.dumps(schedule, ensure_ascii=False),
    }, context_instance = RequestContext(request))


@csrf_exempt
def done(request):
    return JsonResponse({"success" : True})


def edit(request):
    return render_to_response('app_edit.html', {
    }, context_instance = RequestContext(request))

