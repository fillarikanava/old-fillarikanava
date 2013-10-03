"""
Created on 23.3.2009

@author: jsa
"""
from django.conf.urls.defaults import patterns
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver

def decorated_patterns(prefix, fun, *args):
    """
    urls.py addition to allow for logic that spans multiple routes
    Grabbed from http://blog.elsdoerfer.name/2008/01/02/decorating-urlpatterns/
    """
    class DecoratedURLPattern(RegexURLPattern):
        def resolve(self, *args, **kwargs):
            result = RegexURLPattern.resolve(self, *args, **kwargs)
            if result:
                result = list(result)
                result[0] = self._decorate_with(result[0])
            return result

    class DecoratedURLResolver(RegexURLResolver):
        """Inspired by above (with a few lines of copy paste, little annoying..)"""
        def resolve(self, *args, **kwargs):
            result = RegexURLResolver.resolve(self, *args, **kwargs)
            if result:
                result = list(result)
                result[0] = self._decorate_with(result[0])
            return result

    result = patterns(prefix, *args)
    if fun:
        for p in result:
            if isinstance(p, RegexURLPattern):
                p.__class__ = DecoratedURLPattern
                p._decorate_with = fun
            elif isinstance(p, RegexURLResolver):
                p.__class__ = DecoratedURLResolver
                p._decorate_with = fun
    return result
