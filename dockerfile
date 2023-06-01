FROM python:3.9.7-slim-buster

RUN  apt update && apt install -y curl \ 
    && curl -sL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get update && apt-get install -y nodejs && npm install --global yarn

COPY ./api/reqs.txt /app/reqs.txt
WORKDIR /app
RUN pip install -r reqs.txt
EXPOSE 5000
COPY . /app
ENTRYPOINT [ "python3", "app.py"] 