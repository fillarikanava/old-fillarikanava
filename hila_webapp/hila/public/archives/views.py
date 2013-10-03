from django.template.context import RequestContext
from django.utils.datetime_safe import datetime
from hila import roundup_utils
from util import render_with_default
from django.utils.translation import ugettext as _

(_('unread'), _('deferred'), _('chatting'), _('need-eg'),
 _('in-progress'), _('testing'), _('done-cbb'), _('resolved'))

db = roundup_utils.db()

statuses = dict((int(status.id), status.name)
                for status in db.status.getnodes(db.status.list()))
statuses_rev = dict((val, int(key)) for key, val in statuses.items())

def _report_list(year, month, status=None):
    # manual sanitization
    year, month = int(year), int(month)
    dfrom = '%d-%d-1' % (year, month)
    dto = '%d-%d-1' % (year, month + 1)
    sql = """\
        SELECT id FROM _issue
        WHERE _creation >= '%s'
            AND _creation < '%s'""" % (dfrom, dto)
    if status:
        status = int(statuses_rev.get(status, status))
        sql += ' AND _status = %d' % status
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
    archives = [(name, _year_data(int(id)))
                for id, name in statuses.items()]
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
