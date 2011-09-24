import time, pytz
from itertools import chain, groupby
from operator import attrgetter
from datetime import datetime, time

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django import forms
try:
    import json
except:
    import django.utils.simplejson as json
from django.contrib.auth.decorators import login_required

from helpers import stringToEpochMilli
from account.forms import Timezone as TimezoneForm


# Return JSON encoded representation of object as text response
dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime) or isinstance(obj, time) else None
def JsonResponse(obj):
    return HttpResponse(json.dumps(obj, ensure_ascii=False, default=dthandler),
                        mimetype="text/plain; charset=\"utf-8\"")

def about(request):
    return HttpResponseRedirect('/')

def blog(request):
    return HttpResponseRedirect('/')


def contact(request):
    return HttpResponseRedirect('/')

    
@login_required
def home(request, message=None):
    print message
    now = int(time.time()*1000)
    timezone = pytz.timezone(request.user.get_profile().tz)

    return render_to_response('app_home.html', {
        'message'      : message,
    }, context_instance = RequestContext(request))

def flatten(listOfLists):
    "Flatten one level of nesting"
    return chain.from_iterable(listOfLists)

@login_required                              
def meds(request):

    user_profile = request.user.get_profile()
    user_meds = request.user.usermedication_set.all()

    # load schedule for each medication and flatten into one list
    user_med_times = list(flatten([um.usermedicationschedule_set.all() for um in user_meds]))

    schedule = []

    # hash by time
    keyfunc = attrgetter('time_scheduled')    
    user_med_times = sorted(user_med_times, key=keyfunc)
    for (time, meds) in groupby(user_med_times, keyfunc):
        schedule.append({ "time" : time, "meds" : [m.user_med.medication.name for m in meds]})

    return JsonResponse({'schedule' : schedule})
