from django.shortcuts import render_to_response
from django.template.context import RequestContext


def handler500(request):
    return render_to_response('500.html', {}, RequestContext(request))

def handler404(request):
    return render_to_response('404.html', {}, RequestContext(request))
