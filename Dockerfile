FROM python:3.10

EXPOSE 8000

WORKDIR /app

COPY . .

RUN pip install -e .

