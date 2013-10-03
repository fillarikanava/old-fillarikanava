from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from hila.public.profiles.models import UserProfile

class UserProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    
    def __init__(self, instance=None, **kwargs):
        super(UserProfileForm, self).__init__(**kwargs)
        # In case we have an instance, prepopulate the form with the users data
        if instance:
            for key in self.fields.iterkeys():
                if hasattr(instance.user, key):
                    self.fields[key].__setattr__('initial', getattr(instance.user, key)) 
    
    def save(self, commit=False, userobj=None):
        try:
            user = User._default_manager.get(pk=userobj.id)
            profile = UserProfile._default_manager.get(user=user)
        except User.DoesNotExist:
            # This should never happen, but redirect the user to registration anyway.
            HttpResponseRedirect(reverse('signup'))
        except UserProfile.DoesNotExist:
            profile = UserProfile(user=user)

        for key in self.cleaned_data.iterkeys():
            if hasattr(user, key):
                setattr(user, key, self.cleaned_data[key])
            elif hasattr(profile, key):
                setattr(profile, key, self.cleaned_data[key])
        
        user.save()
        profile.save()
        return user