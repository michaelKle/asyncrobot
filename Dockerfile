FROM python:3.12-bookworm

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
