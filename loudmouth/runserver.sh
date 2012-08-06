#!/bin/bash

name=loudmouth
port=9029

if [ `id -u` = 0 ]
then
        echo "DON'T run this as ROOT!"
        exit 1
fi

PROJDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PIDFILE="$PROJDIR/$name.pid"
PYTHONPATH="$PROJDIR:$PYTHONPATH"

cd $PROJDIR
if [ -f $PIDFILE ]; then
    kill $(cat -- $PIDFILE)
    rm -f -- $PIDFILE
fi

if [ "$1" == "stop" ]
then
    exit 0
fi

exec /usr/bin/env \
	PYTHONPATH=$PYTHONPATH \
	LC_ALL="en_US.UTF-8" \
	python $PROJDIR/manage.py runfcgi pidfile=$PIDFILE method=threaded host=127.0.0.1 port=$port

