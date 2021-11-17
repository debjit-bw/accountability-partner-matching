FROM python:3.9-slim-buster
WORKDIR /accountability-partner-matching
COPY . .
RUN pip3 install -r requirements.txt
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app