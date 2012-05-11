#!/bin/bash

PROJECT_ROOT=/home/kirill/astven/projects/suitup
. /home/kirill/astven/envs/suitup/bin/activate
cd $PROJECT_ROOT
python manage.py retry_deferred >> $PROJECT_ROOT/logs/cron_mail_deferred.log 2>&1
