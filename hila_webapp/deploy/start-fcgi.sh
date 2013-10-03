#!/bin/sh

. `dirname $0`/stop-fcgi.sh

$MANAGE runfcgi socket=$SOCKET pidfile=$PIDFILE outlog=$LOG errlog=$LOG
