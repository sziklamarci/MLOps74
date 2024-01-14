# Base image
FROM python:3.11-slim

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*

COPY mlops74/requirements.txt mlops74/requirements.txt
COPY mlops74/pyproject.toml mlops74/pyproject.toml
COPY mlops74/smoke/ mlops74/smoke/
COPY mlops74/data/ mlops74/data/

WORKDIR /mlops74/
RUN pip install -r requirements.txt --no-cache-dir
RUN pip install . --no-deps --no-cache-dir

ENTRYPOINT ["python", "-u", "smoke/train_model.py"]