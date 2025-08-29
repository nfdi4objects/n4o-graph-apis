FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get install -y npm 

COPY . .

WORKDIR /app/static
RUN npm init -y && npm install

WORKDIR /app/


CMD [ "python3", "app.py", "--wsgi" ]
