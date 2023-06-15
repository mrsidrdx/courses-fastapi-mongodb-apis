FROM python:3.11.2-slim-buster

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc \
  && apt-get clean

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Specify the FastAPI environment port
ENV PORT 8000

# By default, listen on port 8000
EXPOSE 8000

# add app
COPY . .

CMD ["/bin/bash", "-c", "python scripts/upload_documents.py;python app/main.py"]