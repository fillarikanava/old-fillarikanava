from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save

from hila import roundup_utils

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    roundup_id = models.IntegerField(unique=True)
    
    def save(self, force_insert=False, force_update=False):
        if self.roundup_id is not None:
            roundup_user = roundup_utils.get_user(username=self.user.username)
            screenname = ' '.join((self.user.first_name, self.user.last_name))
            # Update user
            # we'll leave out address=self.user.email, for now, because roundup will return an exception..
            roundup_utils.update_user(username=self.user.username, id=roundup_user['id'], screenname=screenname, passwd=self.user.password)
        else:
            roundup_uid = roundup_utils.create_user(username=self.user.username, screenname='', address=self.user.email, passwd=self.user.password)
            self.roundup_id = roundup_uid
        super(UserProfile, self).save(force_insert, force_update)

def create_roundup_user(sender=None, instance=None, **kwargs):
    if getattr(instance, "is_active"):
        try:
            userprofile = instance.get_profile()
        except UserProfile.DoesNotExist:
            profile = UserProfile(user=instance)
            profile.save()
            grp = Group._default_manager.get(name__iexact='Citizen')
            instance.groups.add(grp)

post_save.connect(create_roundup_user, sender=User)