#!/bin/bash

PROJECT_ROOT=/home/kirill/astven/projects/suitup
. /home/kirill/astven/envs/suitup/bin/activate
cd $PROJECT_ROOT
python manage.py send_mail >> $PROJECT_ROOT/logs/cron_mail.log 2>&1
