# base image  
FROM python:3.8   

ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

# install dependencies  
RUN pip install --upgrade pip  

# run this command to install all dependencies  
RUN pip install -r requirements.txt  

COPY . code
WORKDIR /code

# port where the Django app runs  
EXPOSE 8000  

# start server  
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000", "--settings=djangoMepML.production_settings"]
