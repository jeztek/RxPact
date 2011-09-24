import time, pytz

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
def JsonResponse(obj):
    return HttpResponse(json.dumps(obj, ensure_ascii=False),
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
                              
