#from datetime import datetime
#from django.core.urlresolvers import reverse
#from hila import roundup_utils
#import random, os, re, datetime
#from django.conf import settings

#from django.utils.translation import ugettext as _
from util.misc_utils import smart_date_diff, issue_to_dict as is2dic, issue_to_quick_dict as is2quickd


def issue_to_dict(issue, issue_id=None, db=None):

    return is2dic(issue, issue_id, db=db)


def issue_to_quick_dict(issue, issue_id=None, db=None):

    return is2quickd(issue, issue_id, db=db)
