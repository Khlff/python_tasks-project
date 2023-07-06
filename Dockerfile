FROM python:3.10
LABEL authors="Khlff"

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
RUN mkdir /app/downloads
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

ENTRYPOINT ["python", "./server_directory/server.py", "-path", "./downloads"]
