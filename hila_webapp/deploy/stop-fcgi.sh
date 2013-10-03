#!/bin/sh

. `dirname $0`/env.sh

if [ -f $PIDFILE ]; then
	kill `cat -- $PIDFILE`
	rm -f -- $PIDFILE
fi
