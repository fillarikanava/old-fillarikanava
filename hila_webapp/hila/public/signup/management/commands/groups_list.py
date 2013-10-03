from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import Group, User
from django.db import IntegrityError

from hila import roundup_utils

class Command(NoArgsCommand):
    help = "Syncronizes organisations from Roundup as groups in Django"
    
    def handle_noargs(self, **options):
        connection = roundup_utils.tracker().open('admin')
        # Get HILA users
#        HILA = User._default_manager.get(groups='1')
#        for 
        organisations = connection.organisation.list()
        print "RoundupID | DjangoID | Groupname"
        print "----------|----------|----------"
        for organisation in organisations:
            org = connection.organisation.getnode(organisation)
            grp = Group._default_manager.get(name=org['name'])
            print "%s | %s | %s" % (org['id'].rjust(9, ' '), str(grp.id).rjust(8, ' '), org['name'])
            