#!/bin/sh

VAR_DIR="$(basedir)/var"
PIDFILE="${VAR_DIR}/$(project)-$(env).pid"
SOCKET="${VAR_DIR}/$(project)-$(env).sock"
LOG="${VAR_DIR}/$(project)-$(env).log"
DEPENDENCIES="$(module_dir) \ # before environment-specific files
              $(module_dir)/deploy/$(env) \
              $(basedir)/Django-1.2.3 \
              $(basedir)/django-multilingual-ng-0.1.20 \
              $(basedir)/roundup-1.4.8"

for dep in $DEPENDENCIES; do
	PYTHONPATH=${PYTHONPATH}:${dep}
done

MANAGE="/usr/bin/env \
		PYTHONPATH=${PYTHONPATH} \
		DJANGO_SETTINGS_MODULE=settings \
		PYTHON_EGG_CACHE=/tmp/egg-cache \
	python2.5 $(module_dir)/manage.py"
