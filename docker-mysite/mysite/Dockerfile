# pull official base image
FROM python:3.7-alpine

# set work directory
WORKDIR /usr/src/app


# copy project
COPY . /usr/src/app


# install dependencies
RUN apk add postgresql-dev
RUN apk add gcc
RUN apk add python3-dev
RUN apk add musl-dev
RUN pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# EXPOSE port 8000 to allow communication to/from server
EXPOSE 8000

# CMD specifcies the command to execute to start the server running.
CMD gunicorn mysite.wsgi:application --bind 0.0.0.0:8000
# CMD python manage.py runserver 0.0.0.0:8000