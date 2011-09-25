import pytz

from django import forms

class Settings(forms.Form):
    timezones = ['US/Pacific', 'US/Central', 'US/Eastern', 'US/Hawaii', \
                 'US/Mountain', 'US/Pacific', 'UTC']
    timezones.extend(pytz.common_timezones)
    tzchoices = [(x, x) for x in timezones]
    tz = forms.ChoiceField(choices = tzchoices)
    phone = forms.CharField()

class Login(forms.Form):
    email    = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
