from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from models import User, UserProfile

from forms import Timezone as TimezoneForm
from forms import Login as LoginForm

@login_required
def settings(request):
    message = None
    if request.method == 'POST':
        form = TimezoneForm(request.POST)
        if form.is_valid():
            tz = form.cleaned_data['tz']
            profile = request.user.get_profile()
            profile.tz = tz
            profile.save()
            return HttpResponseRedirect('/')
        else:
            message = "Invalid time zone selection"
            
    tz = request.user.get_profile().tz
    timezoneForm = TimezoneForm(initial={'tz' : tz})
    return render_to_response('account_settings.html', {
        'message'      : message,
        'timezoneForm' : timezoneForm,
    }, context_instance=RequestContext(request))


def login(request):
    message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email    = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=email, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/')
        else:
            message = "Invalid email or password"
                
    form = LoginForm()
    return render_to_response('account_login.html', {
        'form'    : form,
        'message' : message,
    }, context_instance=RequestContext(request))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

