FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get -y install libpq-dev gcc dos2unix && apt-get clean

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN dos2unix ./entrypoint.sh
RUN chmod +x ./entrypoint.sh
CMD ./entrypoint.sh

EXPOSE 8000
