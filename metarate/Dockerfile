FROM python:3.12-slim
RUN groupadd -r groupmetarate && useradd -r -g groupmetarate usermetarate

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

WORKDIR /app/www/metarate
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

USER usermetarate

#docker run --name metarate -d --network metarate_network -p 8000:4000 --link psgr:dbps -v .:app/www/metarate