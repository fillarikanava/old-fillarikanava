from django.core.management.commands.runserver import Command as RunCommand
from optparse import make_option
from util import nomigrane
import logging, os


class Command(RunCommand):
    option_list = RunCommand.option_list + (
        make_option('--sql-dir', dest='sql_dir', default='sql',
            help='SQL migration file directory'),
    )
    help = 'Applies SQL migration files and ' + RunCommand.help

    def handle(self, *args, **options):
        # from autoreload.py
        if 'RUN_MAIN' not in os.environ:
            logging.basicConfig(level=logging.DEBUG)
            nomigrane.do_migrations(os.path.abspath(options.get('sql_dir', 'sql')),
                                    True)
        super(Command, self).handle(*args, **options)
