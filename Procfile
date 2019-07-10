release: cp main/local.py.example main/local.py
release: python manage.py migrate
web: gunicorn main.wsgi --log-file -
