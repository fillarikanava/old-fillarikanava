from django.contrib import admin
from django.conf.urls.defaults import *

from hila.admin import admin_site
from hila.public.profiles.models import UserProfile

class UserAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'user__first_name')
    
admin_site.register(UserProfile, UserAdmin)