from django.template.context import RequestContext
from util import render_with_default
from util.misc_utils import get_popular_messages, get_latest_messages
from hila import roundup_utils
from hila.api import issue_to_dict

def front(request):
    return render_with_default({}, RequestContext(request))

def map(request):
    return render_with_default({}, RequestContext(request))

def single(request, report_id):

    return render_with_default(
        {'issue' : issue_to_dict(None, report_id) }, 
        RequestContext(request))

    
    
    return render_with_default({}, RequestContext(request))

def latest(request):
    
    latest_messages = get_latest_messages(count=3,offset=0,filters=None)
    
    return render_with_default({'latest_messages': latest_messages,
                                }, RequestContext(request))

def popular(request):
    
    popular_messages = get_popular_messages(count=3,offset=0,filters=None)
    
    return render_with_default({'popular_messages' : popular_messages, 
                                }, RequestContext(request))


#def create(request):
#    raise NotImplementedError