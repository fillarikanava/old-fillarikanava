from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.utils import simplejson

import inspect, os


def render_with_default(*args, **kwargs):
    caller = inspect.getouterframes(inspect.currentframe())[1]
    parent, app = os.path.split(os.path.dirname(caller[1]))
    function = caller[3]
    return render_to_response('%s/%s.html' % (app, function), *args, **kwargs)

def json_resp(fun):
    """Primarily, sets Content-Type to 'application/json' if returned
    object is instance of HttpResponse.

    If returned object is a subclass instance of HttpResponse _and_
    Content-Type is _not_ application/json, then Content-Type is set
    and content itself is wrapped inside JSON object.

    Also, Http404 exceptions are mapped into HttpResponseNotFound
    instances with error message wrapped inside JSON object and content
    type set accordingly.
    """
    def _decorate(request, *args, **kwargs):
        try:
            response = fun(request, *args, **kwargs)
            if type(response) is HttpResponse:
                response['Content-Type'] = 'application/json'
                if not response.content:
                    # same as simplejson.dumps('')
                    response.content = '""'
            elif isinstance(response, HttpResponse) and \
                    response['Content-Type'] != 'application/json':
                response.content = simplejson.dumps({'error': response.content})
                response['Content-Type'] = 'application/json'
        except Http404, err:
            response = HttpResponseNotFound(simplejson.dumps({'error': str(err)}),
                                            mimetype='application/json')
        return response
    return _decorate
