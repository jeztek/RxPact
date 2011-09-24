from django.contrib import admin
from account.models import *

class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile)
