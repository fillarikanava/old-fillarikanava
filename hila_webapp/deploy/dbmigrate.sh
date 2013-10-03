#!/bin/sh

. `dirname $0`/env.sh

$MANAGE migrate $(module_dir)/sql
