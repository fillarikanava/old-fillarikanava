"""
Copied from
http://code.djangoproject.com/svn/django/trunk/django/template/loaders/app_directories.py
"""
from django.conf import settings
from django.template import TemplateDoesNotExist
from django.template.loaders import app_directories
from django.utils._os import safe_join

import os, re


def get_template_sources(template_name, template_dirs=None):
    if not template_dirs:
        template_dirs = app_directories.app_template_dirs
    parts = re.split('[/|\\\\]', template_name)
    if len(parts) > 1:
        app, template_name = parts[0], os.path.join(*parts[1:])
    else:
        app, template_name = None, parts[0]
    for template_dir in template_dirs:
        if template_dir.endswith(app and os.path.join(app, 'templates') or 'templates'):
            try:
                yield safe_join(template_dir, template_name)
            except ValueError:
                # The joined path was located outside of template_dir.
                pass

def load_template_source(template_name, template_dirs=None):
    for filepath in get_template_sources(template_name, template_dirs):
        try:
            return (open(filepath).read().decode(settings.FILE_CHARSET), filepath)
        except IOError:
            pass
    raise TemplateDoesNotExist, template_name
load_template_source.is_usable = True
