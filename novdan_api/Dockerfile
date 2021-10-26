FROM python:3.10

RUN apt-get update && \
    apt-get upgrade -y

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

# by default run with dev settings
ENV DJANGO_SETTINGS_MODULE=novdan_api.settings.dev

# by default run the dev server
CMD python manage.py runserver 0.0.0.0:8000
