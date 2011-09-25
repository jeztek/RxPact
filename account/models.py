from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import pluralize

from forms import Settings as SettingsForm


# Customized QuerySet and Manager adapted from:
# http://davyd.livejournal.com/262241.html
class SerializedQuerySet(models.query.QuerySet):
    def __init__ (self, model = None, *args, **kwargs):
        super(SerializedQuerySet, self).__init__ (model, *args, **kwargs)

    def serialize(self):
        return [e.serialize() for e in self]

    def with_colors(self):
        return [e.with_colors() for e in self]


class SerializedManager(models.Manager):
    def __init__ (self, *args, **kwargs):
        super(SerializedManager, self).__init__ (*args, **kwargs)
		
    def get_query_set(self):
        return SerializedQuerySet(self.model)
	
    def serialize(self):
        return self.get_query_set().serialize()


class UserProfile(models.Model):
    user  = models.ForeignKey(User, unique=True)
    tz    = models.CharField(max_length=50, choices=SettingsForm.tzchoices)
    phone = models.CharField(max_length=10)
    picture_name = models.CharField(max_length=50, null=True)
    score = models.IntegerField()

    def __unicode__(self):
        return self.user.username

class UserNetwork(models.Model):
    user = models.ForeignKey(User, related_name='user')
    link = models.ForeignKey(User, related_name='link')

    objects = SerializedManager()
    
    def with_colors(self):
        score = self.link.get_profile().score
        red = int(-255/100.0*score + 255.0) * 65536
        green = int(255/100.0*score) * 256
        self.color = "#%0.6X" % (red + green)
        return self
    
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
    
