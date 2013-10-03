from django.contrib import admin
from hila.admin import admin_site

from hila.public.signup.models import RegistrationProfile


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'activation_key_expired')
    search_fields = ('user__username', 'user__first_name')


admin_site.register(RegistrationProfile, RegistrationAdmin)
