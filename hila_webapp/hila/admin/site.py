from django.contrib import admin

from django.contrib.admin.sites import AdminSite
from django.db import models


#admin_site = AdminSite()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.sites.models import Site
from hila.public.report.models import Theme
from hila.api.models import Apikey

#from hila.admin import admin_site

admin.site.register(User)
admin.site.register(Group)

admin.site.register(Permission)
admin.site.register(Apikey)
admin.site.register(Site)

from multilingual.admin import MultilingualModelAdmin

class ThemeEntryAdmin(MultilingualModelAdmin):
    pass

admin.site.register(Theme, ThemeEntryAdmin)
#admin_site.register(Theme)
