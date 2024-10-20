FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update && apt-get install -y gcc default-libmysqlclient-dev pkg-config

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
