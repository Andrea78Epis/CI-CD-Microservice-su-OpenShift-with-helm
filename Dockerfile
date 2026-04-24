FROM python:3.10

WORKDIR /app

COPY app/ /app/

RUN pip install flask

EXPOSE 8080

CMD ["python", "app.py"]
