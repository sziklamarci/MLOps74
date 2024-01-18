# Base image
FROM python:3.11-slim

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*

WORKDIR /mlops74/

COPY ../requirements.txt .
COPY ../pyproject.toml .
COPY ../smoke/ smoke/
COPY ../data/ data/


RUN pip install -r requirements.txt --no-cache-dir
RUN pip install . --no-deps --no-cache-dir

ENTRYPOINT ["python", "-u", "smoke/predict_model.py"]