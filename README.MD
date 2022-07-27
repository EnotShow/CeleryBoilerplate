celery -A config worker -B --loglevel=info -P eventlet
celery -A config flower
