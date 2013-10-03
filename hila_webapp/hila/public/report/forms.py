from django import forms
from django.forms.widgets import Textarea
from captcha.fields import CaptchaField

class CaptchaForm(forms.Form):
    captcha = CaptchaField()


class ReportForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(),max_length=140, required=True)

class DetailsForm(forms.Form):   
    details = forms.CharField(widget=forms.Textarea(),max_length=2000, required=False)

class KeywordsForm(forms.Form):   
    keywords = forms.CharField(required=False,widget=forms.HiddenInput)

class GeodataForm(forms.Form):       
    issueaddress = forms.CharField(required=False)
    issuelng = forms.CharField(required=False, widget=forms.HiddenInput)
    issuelat = forms.CharField(required=False, widget=forms.HiddenInput)
    issuepostal = forms.CharField(required=False, widget=forms.HiddenInput)
    issuecity = forms.CharField(required=False, widget=forms.HiddenInput)
    issuecountry = forms.CharField(required=False, widget=forms.HiddenInput)
#    issuedirection = forms.Charfield(required=False, widget=forms.HiddenInput)

class UserdataForm(forms.Form):       
    userfullname = forms.CharField(max_length=100)
    useremail = forms.EmailField(required=False)

class CommentForm(forms.Form):
#    anonname = forms.CharField(required=False)
#    anonurl = forms.URLField(required=False)
    comment = forms.CharField(widget=forms.Textarea(), required=False)

class FileUploadForm(forms.Form):
    file = forms.FileField (required=False  )

class SearchForm(forms.Form):
    search = forms.CharField(max_length=140, required=False)
#    updatemap = forms.TypedChoiceField(coerce=bool,
#                   choices=((False, 'Constrain search to map'), (True, 'Refresh map with search results')),
#                   widget=forms.RadioSelect )
#    campaign =  forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label="", required=False)