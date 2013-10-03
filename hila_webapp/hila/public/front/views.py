from django.conf import settings
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.datetime_safe import datetime
from django.core.urlresolvers import reverse
from hila import roundup_utils
#from hila.api import issue_to_dict,reverse
from util.misc_utils import get_popular_messages, get_latest_messages, get_officer_messages,get_tag_decorations

from util import render_with_default


from django.conf import settings
from django.http import Http404
from roundup import instance
from roundup import password

try:
    import xapian
    xapian_avail = True
except ImportError:
    logging.warning('Failed to import xapian, search disabled')
    xapian_avail = False


def front(request):
    
    if not request.session.has_key('first_visit'):
        request.session.setdefault('first_visit', 1)
        first_visit=1
    else:
        first_visit=None
    
    
    
    if not request.session.has_key('first_visit'):
        request.session.setdefault('first_visit', 1)
        first_visit=1
    else:
        first_visit=None
    
#    try:
#        popular_messages = get_popular_messages(count=7,offset=0,filters=None)
#    except:
#        print "ERROR in getting popular messages!"
    popular_messages = {}

    latest_messages = get_latest_messages(count=7,offset=0,filters=None)              

    officer_messages = get_officer_messages(count=7,offset=0,filters=None,organisations=[4,6])

    # oh my kludg!  What a mess I'm making here...
    # print "Let's go through the officer messages_"
    for i in range(0, len(officer_messages)):
        cc = len(officer_messages[i]["options"]["comments"])
        for j in range (0, cc):
            org = int(officer_messages[i]["options"]["comments"][cc-j-1]["organisation"]["id"])
            if   org >= 4:
                officer_messages[i]["options"]["comments"][cc-j-1].update( {"official": True} )
            else: 
                officer_messages[i]["options"]["comments"].pop(cc-j-1)


    try:    
        archives = [ _year_data(int(0))]
    except:
       print "ERROR in creating archives!"
       archives = []    

    
    return render_with_default({'popular_messages' : popular_messages, 
                                'latest_messages': latest_messages,
                                'officer_messages': officer_messages,
                                'first_visit': first_visit,
                                'archives': archives,
                                'decorations': None,
                                }, RequestContext(request))



def talvikysely(request):
    themed(request, "talvikysely")


def themed(request, theme):

    if not request.session.has_key('first_visit'):
        request.session.setdefault('first_visit', 1)
        first_visit=1
    else:
        first_visit=None
    
    
    if not request.session.has_key('first_visit'):
        request.session.setdefault('first_visit', 1)
        first_visit=1
    else:
        first_visit=None

#    try:
#        print "aa" + [1]
#        popular_messages = get_popular_messages(count=7,offset=0,filters=None)
#    except:
#        print "ERROR in getting popular messages!"
        
    popular_messages = {}
        


    latest_messages = get_latest_messages(count=7,offset=0,filters=None,tag="talvikysely")

    officer_messages = get_officer_messages(count=7,offset=0,filters=None,organisations=[4,6],tag="talvikysely")

    # oh my kludg!  What a mess I'm making here...
    # print "Let's go through the officer messages_"
    for i in range(0, len(officer_messages)):
        cc = len(officer_messages[i]["options"]["comments"])
        for j in range (0, cc):
            org = int(officer_messages[i]["options"]["comments"][cc-j-1]["organisation"]["id"])
            if   org >= 4:
                officer_messages[i]["options"]["comments"][cc-j-1].update( {"official": True} )
            else: 
                officer_messages[i]["options"]["comments"].pop(cc-j-1)


    try:    
        archives = [ _year_data(int(0))]
    except:
       archives = []



    return render_with_default({'popular_messages' : popular_messages,
                                'latest_messages': latest_messages,
                                'officer_messages': officer_messages,
                                'first_visit': first_visit,
                                'archives': archives,
                                'decorations': get_tag_decorations(theme)
                                }, RequestContext(request))


def betafront(request):
    
    if not request.session.has_key('first_visit'):
        request.session.setdefault('first_visit', 1)
        first_visit=1
    else:
        first_visit=None
    
    
    
    if not request.session.has_key('first_visit'):
        request.session.setdefault('first_visit', 1)
        first_visit=1
    else:
        first_visit=None
    
    try:
        popular_messages = get_popular_messages(count=7,offset=0,filters=None)
    except:
        print "ERROR in getting popular messages!"
        popular_messages = {}
    try:
        latest_messages = get_latest_messages(count=7,offset=0,filters=None)        
        
    except:
        print "ERROR in getting latest messages!"
        latest_messages = {}
    officer_messages = get_officer_messages(count=7,offset=0,filters=None,organisations=[4,6])
    for i in range(0, len(officer_messages)):
            for j in range (0, len(officer_messages[i]["options"]["comments"])):
                org = int(officer_messages[i]["options"]["comments"][j]["organisation"]["id"])
                if   org >= 4:
                    officer_messages[i]["options"]["comments"][j].update( {"official": True} )
                    break;

    try:    
        archives = [ _year_data(int(0))]
    except:
       print "ERROR in creating archives!"
       archives = []    

    
    return render_with_default({'popular_messages' : popular_messages, 
                                'latest_messages': latest_messages,
                                'officer_messages': officer_messages,
                                'first_visit': first_visit,
                                'archives': archives,
                                }, RequestContext(request))

def settings(request):
    return render_to_response('settings.js', {}, RequestContext(request))

def advice(request):
    return render_with_default({}, RequestContext(request))

def contact(request):
    return render_with_default({}, RequestContext(request))

def feedback(request):
    return render_with_default({}, RequestContext(request))

def info(request):
    return render_with_default({}, RequestContext(request))

def media(request):
    return render_with_default({}, RequestContext(request))

def privacy(request):
    return render_with_default({}, RequestContext(request))




from django.utils.translation import ugettext as _

#(_('unread'), _('deferred'), _('chatting'), _('need-eg'),
# _('in-progress'), _('testing'), _('done-cbb'), _('resolved'))

db = roundup_utils.db()

#statuses = dict((int(status.id), status.name)
#                for status in db.status.getnodes(db.status.list()))
#statuses_rev = dict((val, int(key)) for key, val in statuses.items())

def _report_list(year, month, status=None):
    # manual sanitization
    year, month = int(year), int(month)
    dfrom = '%d-%d-1' % (year, month)
    dto = '%d-%d-1' % (year, month + 1)
    sql = """\
        SELECT id FROM _issue
        WHERE _creation >= '%s'
            AND _creation < '%s'""" % (dfrom, dto)
#    if status:
#        status = int(statuses_rev.get(status, status))
#        sql += ' AND _status = %d' % status
    id_list = [str(r[0]) for r in db.issue.filter_sql(sql)]
    return db.issue.getnodes(id_list)

def _month_data(year, status=None):
    now = datetime.now()
    def list(month):
        if now.year == year and now.month == month:
            return _report_list(year, month, status)
        return None
    r = range(year == now.year and now.month or 12, 0, -1)
    return [(month, list(month)) for month in r]

def _year_data(status):
    return [(year, _month_data(year, status))
            for year in range(datetime.now().year, 2008, - 1)]

def date_index(request):
    return render_with_default({}, RequestContext(request))

def by_date(request, year, month):
    return render_with_default({}, RequestContext(request))

def status_index(request):
    archives = [(0, _year_data(int(0))) ]
    return render_with_default(
        {'archives': archives},
        RequestContext(request))

def by_status(request, status):
    raise NotImplementedError

def search(request):
    raise NotImplementedError

def for_date(request, year, month):
    return render_with_default(
        {'reports': _report_list(int(year), int(month), request.GET.get('status', None)),},
        RequestContext(request))

