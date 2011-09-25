from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from models import User, UserProfile

from forms import Settings as SettingsForm
from forms import Login as LoginForm

@login_required
def settings(request):
    message = None
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            tz = form.cleaned_data['tz']
            phone = form.cleaned_data['phone']
            profile = request.user.get_profile()
            profile.tz = tz
            profile.phone = phone
            profile.save()
            return HttpResponseRedirect('/')
        else:
            message = "Invalid time zone selection or phone number"

    profile = request.user.get_profile()
    settingsForm = SettingsForm(initial={'tz' : profile.tz,
                                         'phone' : profile.phone})
    return render_to_response('account_settings.html', {
        'message'      : message,
        'settingsForm' : settingsForm,
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

