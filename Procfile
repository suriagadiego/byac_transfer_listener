web: celery -A bayc_event worker -E -l info & celery -A bayc_event beat --loglevel=info & gunicorn byac_event.wsgi --log-file
