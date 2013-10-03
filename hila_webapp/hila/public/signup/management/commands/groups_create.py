from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import Group
from django.db import IntegrityError

from hila import roundup_utils

class Command(NoArgsCommand):
    help = "Syncronizes organisations from Roundup as groups in Django"
    
    def handle_noargs(self, **options):
        connection = roundup_utils.tracker().open('admin')
        organisations = connection.organisation.list()
        for organisation in connection.organisation.list():
            org = connection.organisation.getnode(organisation)
            grp = Group(name=org['name'])
            try:
                grp.save()
            except IntegrityError:
                # Group already exists, no need to add it
                pass