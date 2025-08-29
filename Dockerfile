FROM nikolaik/python-nodejs:python3.13-nodejs22-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

WORKDIR /app/static
RUN npm init -y && npm install

WORKDIR /app/


CMD [ "python3", "app.py", "--wsgi" ]
