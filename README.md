Setup Instructions:

step 1 : Run pip install -r requirements.txt to install dependencies
step 2 : Create a .env file with following variables
        DB_NAME=
        DB_USER=
        DB_PASSWORD=
        DB_HOST=
        DB_PORT=
step 3 : Run python manage.py migrate
step 4 : Run python manage.py runserver