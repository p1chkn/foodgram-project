FROM python:3.7.3

WORKDIR /code
COPY . .
RUN pip install -r requirements.txt
RUN python manage.py migrate && python manage.py collectstatic