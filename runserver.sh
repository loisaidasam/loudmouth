#!/bin/bash

name=loudmouth
port=9029

if [ `id -u` = 0 ]
then
        echo "DON'T run this as ROOT!"
        exit 1
fi

# Replace these settings.
#PROJDIR="/Users/sam/Source/workspace/loudmouth"
PROJDIR="/home/sam/$name"
PIDFILE="$PROJDIR/$name.pid"
PYTHONPATH="$PROJDIR:$PROJDIR/$name:$PYTHONPATH"

cd $PROJDIR
if [ -f $PIDFILE ]; then
    kill $(cat -- $PIDFILE)
    rm -f -- $PIDFILE
fi

if [ "$1" == "stop" ]
then
    exit 0
fi

if [ "$1" == "debug" ]
then
        #screen -S $name -L /usr/bin/env - LC_ALL="en_US.UTF-8" PYTHONPATH=$PYTHONPATH $PROJDIR/$name/manage.py runfcgi pidfile=$PIDFILE method=threaded host=127.0.0.1 port=$port daemonize=false
        screen -S $name -L /usr/bin/env LC_ALL="en_US.UTF-8" PYTHONPATH=$PYTHONPATH $PROJDIR/$name/manage.py runfcgi pidfile=$PIDFILE method=threaded host=127.0.0.1 port=$port daemonize=false
else
        #exec /usr/bin/env - \
        exec /usr/bin/env \
          PYTHONPATH=$PYTHONPATH \
          LC_ALL="en_US.UTF-8" \
          python $PROJDIR/$name/manage.py runfcgi pidfile=$PIDFILE method=threaded host=127.0.0.1 port=$port
fi

