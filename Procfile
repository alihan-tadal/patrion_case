release: cd app && python manage.py collectstatic --noinput && python manage.py migrate
web: gunicorn --chdir ./app app.wsgi 
