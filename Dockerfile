FROM python:3.9

WORKDIR /app

COPY . /app/

RUN pip install -r /app/requirements

EXPOSE 8000

CMD ["python", "/app/chess_tournament/manage.py", "runserver", "0.0.0.0:8000"]
