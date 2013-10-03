import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

from hila.public.signup.models import RegistrationProfile

attrs_dict = { 'class': 'required' }

class RegistrationForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$', max_length=30, widget=forms.TextInput(attrs=attrs_dict), label=_(u'username'))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=75)), label=_(u'email address'))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False), label=_(u'password'))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False), label=_(u'password (again)'))
    
    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_(u'This username is already taken. Please choose another.'))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u'You must type the same password each time'))
        return self.cleaned_data
    
    def save(self):
        new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['username'], password=self.cleaned_data['password1'], email=self.cleaned_data['email'])
        return new_user

class RegistrationFormUniqueEmail(RegistrationForm):
    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_(u'This email address is already in use. Please supply a different email address.'))
        return self.cleaned_data['email']

class ActivationRequestForm(forms.Form):
    email = forms.EmailField(label=_(u'email address'), max_length=75)
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        self.users_cache = User.objects.filter(email__iexact=email)
        if len(self.users_cache) == 0:
            raise forms.ValidationError(_("That e-mail address doesn't have an associated user account. Are you sure you've registered?"))
        
        for user in self.users_cache:
            registration_profile = RegistrationProfile.objects.get(user=user)
            if registration_profile.activation_key == registration_profile.ACTIVATED:
                raise forms.ValidationError(_("Your account has already been activated."))
    
    def save(self):
        from django.core.mail import send_mail
        for user in self.users_cache:
            registration_profile = RegistrationProfile.objects.get(user=user)
            current_site = Site.objects.get_current()
            
            # Update the users date_joined (and last login) when requesting new activation link so it won't expire right away.
            user.date_joined = datetime.datetime.now()
            user.last_login = datetime.datetime.now()
            user.save()
            
            subject = render_to_string('activation_request_email_subject.txt',
                                         { 'site': current_site })
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())

            message = render_to_string('activation_request_email.txt',
                                         { 'activation_key': registration_profile.activation_key,
                                           'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                                           'site': current_site,
                                           'site_url': settings.SITE_URL })

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])