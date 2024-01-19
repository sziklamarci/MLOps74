# Base image
FROM python:3.11-slim

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*
RUN apt-get update && \
    apt-get install -y libglib2.0-0 libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*

RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && apt-get update -y && apt-get install google-cloud-sdk -y

RUN echo ${{ secrets.DOCKER_SERVICE_ACCOUNT_KEY }} > /tmp/key.json \
    gcloud auth activate-service-account --key-file=/tmp/key.json

RUN pip install dvc \
    pip install "dvc[gs]" \
    pip install "dvc[gdrive]" \
    dvc pull

WORKDIR /

COPY /mlops74/requirements.txt /mlops74/requirements.txt
COPY /mlops74/pyproject.toml /mlops74/pyproject.toml
COPY /mlops74/smoke/ /mlops74/smoke/
RUN cd mlops74/ \
    ls -a
COPY data/ /mlops74/data/
COPY /mlops74/models/ /mlops74/models/

RUN pip install -r mlops74/requirements.txt --no-cache-dir
RUN pip install . --no-deps --no-cache-dir

ENTRYPOINT ["python", "-u", "mlops74/smoke/train_model2.py"]