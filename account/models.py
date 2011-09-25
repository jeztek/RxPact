from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import pluralize

from forms import Timezone as TimezoneForm

class UserProfile(models.Model):
    user  = models.ForeignKey(User, unique=True)
    tz    = models.CharField(max_length=50, choices=TimezoneForm.choices)
    phone = models.CharField(max_length=10)

    def __unicode__(self):
        return self.user.username

class Medication(models.Model):
    name = models.CharField(max_length=50)

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
            "img" : '/img/%s.png' % self.user_med.medication.name.lower().replace(' ', ''),
            "dose" : str(self.dosage_count) + " " + self.dosage + pluralize(self.dosage_count),
            }

class UserMedicationLog(models.Model):
    user_med = models.ForeignKey(UserMedication)
    time_scheduled = models.DateTimeField()
    time_taken = models.DateTimeField()
