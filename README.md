# MepML

Errors may occur when installing *mysqlclient*

# How to run

clone the repo  
`$ git clone git@github.com:MEP-org/MepML_Backend.git`   
create a python virtual environment  
`python3 -m venv venv`  
enter environment  
`source venv/bin/activate`  
install dependencies  
`pip install -r requirements.txt`  

Now you have 2 options:
### Running with local database
`python3 manage.py makemigrations --settings=djangoMepML.development_settings`  
`python3 manage.py migrate --run-syncdb --settings=djangoMepML.development_settings`  
`python3 manage.py database_init --settings=djangoMepML.development_settings `  
`python3 manage.py runserver --settings=djangoMepML.development_settings`  

### Running with remote database
`python3 manage.py runserver`  

### IMPORTANT: Project branches

```main```: production code (when there is a new release)

```dev```: from which we will create feature branches.
