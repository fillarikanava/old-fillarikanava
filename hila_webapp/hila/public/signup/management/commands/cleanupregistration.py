from django.core.management.base import NoArgsCommand

from hila.public.signup.models import RegistrationProfile

class Command(NoArgsCommand):
    help = "Delete expired user registrations from the database"

    def handle_noargs(self, **options):
        RegistrationProfile.objects.delete_expired_users()
