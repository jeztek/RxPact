from django.db import models
from django.contrib.auth.models import User

from forms import Timezone as TimezoneForm

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    tz   = models.CharField(max_length=50, choices=TimezoneForm.choices)

    def __unicode__(self):
        return self.user.username

