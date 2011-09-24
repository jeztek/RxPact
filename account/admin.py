from django.contrib import admin
from account.models import *

class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile)
admin.site.register(Medication)
admin.site.register(UserMedication)
admin.site.register(UserMedicationSchedule)
admin.site.register(UserMedicationLog)
