from django.template.context import RequestContext
from hila.roundup_utils import db
from util import render_with_default


roundup = db()

def timemap(request):
    return render_with_default({}, RequestContext(request))
