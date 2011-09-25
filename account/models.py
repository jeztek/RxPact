from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import pluralize

from forms import Settings as SettingsForm

class UserProfile(models.Model):
    user  = models.ForeignKey(User, unique=True)
    tz    = models.CharField(max_length=50, choices=SettingsForm.tzchoices)
    phone = models.CharField(max_length=10)
    picture_name = models.CharField(max_length=50, null=True)

    def __unicode__(self):
        return self.user.username

class UserNetwork(models.Model):
    user = models.ForeignKey(User, related_name='user')
    link = models.ForeignKey(User, related_name='link')

    def __unicode__(self):
        return unicode(self.user.username)

class Medication(models.Model):
    name = models.CharField(max_length=50)
    picture_name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class UserMedication(models.Model):
    user = models.ForeignKey(User)
    medication = models.ForeignKey(Medication)

    def __unicode__(self):
        return unicode(self.user) + " " + unicode(self.medication)

class UserMedicationSchedule(models.Model):
    user_med = models.ForeignKey(UserMedication)
    time_scheduled = models.TimeField()
    dosage_count = models.IntegerField()
    dosage = models.CharField(max_length=50)

    def __unicode__(self):
        return unicode(self.user_med) + " @ " + unicode(self.time_scheduled)

    def to_dict(self):
        return {
            "name" : self.user_med.medication.name, 
            "picture_name" : self.user_med.medication.picture_name,
            "dose" : str(self.dosage_count) + " x " + self.dosage,
            }

class UserMedicationLog(models.Model):
    user_med = models.ForeignKey(UserMedication)
    time_scheduled = models.DateTimeField()
    time_taken = models.DateTimeField()

    def __unicode__(self):
        return unicode(self.user_med)
    
