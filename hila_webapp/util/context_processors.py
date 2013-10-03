'''
Created on 23.3.2009

@author: jsa
'''
from django.utils import dates

def settings(request=None):
    from django.conf import settings
    return {'settings': settings,}

def locale_constants(request=None):
    return {'WEEKDAYS': dates.WEEKDAYS,
            'MONTHS': dates.MONTHS,
            }
