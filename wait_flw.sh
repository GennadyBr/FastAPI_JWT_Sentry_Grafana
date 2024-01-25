#!/bin/sh
sleep 10
celery --broker=redis://redis_2401:6379 flower --url-prefix='/flower_2401'
