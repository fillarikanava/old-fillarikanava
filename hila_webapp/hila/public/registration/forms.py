from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from hila import roundup_utils
from roundup.password import Password

class RegistrationForm(forms.Form):
    username = forms.CharField(forms.TextInput(), label=_(u'Username'))
    email = forms.EmailField(forms.TextInput(attrs=dict(maxlength=75)), label=_(u'E-mail address'))
    screenname = forms.CharField(forms.TextInput(), label=_(u'Realname'))
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False), label=_(u'Password'))
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False), label=_(u'Confirm password'))
    
    def clean_username(self):
        try:
            user = roundup_utils.test_uniqueness(field='username', value=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_(u'This username is already taken. Please choose another.'))
    
    def clean_email(self):
        try:
            user = roundup_utils.test_uniqueness(field='address', value=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(_(u'E-mail address already in use.'))
    
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u'Password and Confirm password must match.'))
        return self.cleaned_data
    
    def save(self):
        user = roundup_utils.create_user(userdata=dict(username=self.cleaned_data['username'], screenname=self.cleaned_data['screenname'], address=self.cleaned_data['email'], password=self.cleaned_data['password1']))
        return user