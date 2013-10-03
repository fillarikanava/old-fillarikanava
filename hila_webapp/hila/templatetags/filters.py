'''
Created on 31.3.2009

@author: jsa
'''

from django.template import Library

register = Library()

@register.filter
def get(dict, key):
    return dict[key]
