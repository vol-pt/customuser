FROM python:3
ENV DJANGO_SETTINGS_MODULE=customuser.settings
RUN mkdir /app
COPY . /app
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python-pip
RUN pip install django
WORKDIR /app
RUN python manage.py runserver 0.0.0.0:8080
EXPOSE 8080
