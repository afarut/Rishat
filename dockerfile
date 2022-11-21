FROM python:3.9

ENV TZ=Europe/Moscow

RUN mkdir /app
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt 

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]