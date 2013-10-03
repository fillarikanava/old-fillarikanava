from django.http import HttpResponse
from django.template.context import RequestContext
from hila.roundup_utils import db
from util import json_resp, render_with_default


roundup = db()

def timemap(request):
    return render_with_default({}, RequestContext(request))

@json_resp
def filter_save(request):
    return HttpResponse()


def listview(request):
    return render_with_default({}, RequestContext(request))
