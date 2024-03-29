# base image  
FROM python:3.10   

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt requirements.txt

# install dependencies  
RUN pip install --no-cache-dir --upgrade pip  

# run this command to install all dependencies  
RUN pip install --no-cache-dir -r requirements.txt  

COPY . . 

# port where the Django app runs  
EXPOSE 8080  

# start server  
#CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080", "--settings=djangoMepML.production_settings"]
#CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 app.wsgi:application
#CMD ["python3", "manage.py", "makemigrations", "--settings=djangoMepML.production_settings"]  
#CMD ["python3", "manage.py", "migrate", "--run-syncdb", "--settings=djangoMepML.production_settings"]  
#CMD ["python3", "manage.py", "database_init", "--settings=djangoMepML.production_settings"]

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "djangoMepML.wsgi:application", \
    "--log-level=info", "--error-logfile=-", "--workers=2", "--env", "DJANGO_SETTINGS_MODULE=djangoMepML.production_settings"]
