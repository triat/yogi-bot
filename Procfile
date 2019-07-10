release: cp main/local.py.example main/local.py
release: ln -s requirements.txt requirements/prod.txt
release: python manage.py migrate
web: gunicorn main.wsgi --log-file -
