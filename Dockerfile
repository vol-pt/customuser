FROM ubuntu
ENV DJANGO_SETTINGS_MODULE=customuser.settings
RUN mkdir /app
COPY . /app
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python-pip
RUN pip install --upgrade pip
RUN pip install django
RUN pip install python-dateutil
WORKDIR /app
RUN python manage.py runserver 0.0.0.0:8080
EXPOSE 8080
