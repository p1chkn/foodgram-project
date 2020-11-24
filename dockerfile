FROM python:3.7.3

WORKDIR /code
COPY . .
RUN pip install -r requirements.txt
CMD python manage.py migrate && python manage.py collectstatic