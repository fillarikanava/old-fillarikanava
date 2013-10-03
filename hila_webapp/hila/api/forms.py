'''
Created on 16.4.2009

@author: jsa
'''

from django import forms


class SearchForm(forms.Form):
    coords = forms.RegexField(r'(,?\-?\d+){4}', required=False)
    nosy = forms.BooleanField(required=False)
    org_active = forms.BooleanField(required=False)
    org_queue = forms.BooleanField(required=False)
    phrase = forms.CharField(required=False)
    tags = forms.RegexField(r'( ?[\w\-]+)+', required=False)
    queue = forms.RegexField(r'( ?\w+)+', required=False)
    min_priority = forms.ChoiceField(tuple((k, k) for k in ('normal', 'elevated', 'urgent')),
                                     required=False)
    status = forms.ChoiceField(tuple((k, k) for k in ('chatting', 'rfc', 'merged', 'closed')),
                               required=False)
    ordering = forms.ChoiceField(tuple((k, k) for k in ('popularity', 'status', 'report_date', 'comment_date')),
                                 required=False)
    new_first = forms.BooleanField(required=False)
