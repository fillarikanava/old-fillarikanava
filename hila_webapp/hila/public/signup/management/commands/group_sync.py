from django.core.management.base import LabelCommand
from django.contrib.auth.models import Group, User
from django.db import IntegrityError

from hila import roundup_utils

class Command(LabelCommand):
    help = "Syncronizes organisations from Roundup as groups in Django"
    
    def handle_label(self, label, **options):
        try:
            int(label)
        except ValueError:
            print "Please pass in an integer from the group list, which you can get by doing 'python manage.py groups_list'."
            return None

        group_id = str(label)
        db = roundup_utils.tracker().open('admin')

        try:
            users = User._default_manager.filter(groups=group_id)
        except Exception:
            print "No users to sync in that group."
            return None

        if len(users) == 0:
            print "No users to sync in that group."
        else:
            org = db.organisation.getnode(group_id)
            for user in users:
                roundup_id = str(user.get_profile().roundup_id)
                print "Syncing %s in to %s" % (user.username, org['name'])
                organisation = [group_id]
                db.user.set(roundup_id, organisation=organisation)
            db.commit()