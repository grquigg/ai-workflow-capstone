FROM python:3.10.8

WORKDIR /app

ADD . /app

# RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

ENV NAME World

CMD ["python", "app.py"]