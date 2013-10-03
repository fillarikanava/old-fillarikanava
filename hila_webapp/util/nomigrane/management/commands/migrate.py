'''
Created on 26.3.2009

@author: jsa
'''

from django.core.management.commands.runserver import BaseCommand
from util import nomigrane
import logging, os


class Command(BaseCommand):
    help = 'Applies SQL migration files'
    args = "[sqldir='sql']"

    def handle(self, sql_dir='sql', *args, **options):
        logging.basicConfig(level=logging.DEBUG)
        nomigrane.do_migrations(os.path.abspath(sql_dir), True)
