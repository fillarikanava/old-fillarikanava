'''
Created on 1.4.2009

@author: jsa
'''
from django.contrib.auth.models import User

from hila import roundup_utils
from roundup.password import Password

db = roundup_utils.db()

class RoundupUser(User):
    def __init__(self, usernode):

        super(RoundupUser, self).__init__(
            id=usernode.id,
            username=usernode.username,
            first_name=usernode.screenname,
            last_name="",
            email=usernode.address,
            password=None,
            is_staff=False,
            is_active=True,
            is_superuser=False,
#    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True,
#        help_text=_("In addition to the permissions manually assigned, this user will also get all permissions granted to each group he/she is in."))
#    user_permissions = models.ManyToManyField(Permission, verbose_name=_('user permissions'), blank=True)
        )
        
        self.usernode = usernode

    def save(self):
        print "called backends.py RoundupUser.save()"
        pass

class RoundupBackend(object):
    """
    Authenticates against RoundUp user database.
    """
    def authenticate(self, username=None, password=None):
        db = roundup_utils.db()
        try:
            usernode = db.user.getnode(db.user.lookup(username))
            if usernode.password == Password(password):
                print "Authentication successful!"
                return RoundupUser(usernode)
            else:
                print "Authentication failure!"
        except KeyError:
            pass
        return None

    def get_permissions_for_group(self, group):
        return {
            'organisation': ['organisation.access', 'public.report.modify_priority'],
        }.get(group, {})

#    def get_group_permissions(self, user_obj):
#        perms = reduce(lambda role, roles: roles + self.get_permissions_for_group(role),
#                       [],
#                       [role.strip().lower() for role in
#                        user_obj.usernode.roles.split(',')])
#        if user_obj.usernode.organisation:
#            perms += self.get_permissions_for_group('organisation')
#        return perms
#
#    def get_all_permissions(self, user_obj):
#        return self.get_group_permissions(user_obj)
#
    def has_perm(self, user_obj, perm):
        return perm in self.get_all_permissions(user_obj)

    def has_module_perms(self, user_obj, app_label):
        """
        Returns True if user_obj has any permissions in the given app_label.
        """
        for perm in self.get_all_permissions(user_obj):
            if perm[:perm.index('.')] == app_label:
                return True
        return False

    def get_user(self, user_id):
        if db.user.hasnode(user_id):
            return RoundupUser(db.user.getnode(user_id))
        else:
            return roundup_utils.get_user_by_name('anonymous')

