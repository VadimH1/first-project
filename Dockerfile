FROM python:3.10-slim
WORKDIR .

RUN apt-get update && apt-get -y upgrade

COPY requirements.txt .
RUN  pip3 install -r requirements.txt

COPY . .

WORKDIR /first_app
RUN ls -la

EXPOSE 5000

CMD flask run --host=0.0.0.0