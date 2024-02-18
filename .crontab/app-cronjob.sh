#!/bin/sh
#
@weekly python /code/manage.py runcrons > /var/log/cronjob.log
