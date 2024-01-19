FROM python:3.11

WORKDIR /usr/src/app
COPY mlops74/requirements_fast.txt /requirements_fast.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --upgrade pip
RUN pip install --upgrade -r /requirements_fast.txt
RUN pip install fastapi
RUN pip install python-multipart
COPY mlops74/smoke/myfastapi /usr/src/app/myfastapi
COPY mlops74/smoke/models /usr/src/app/models

CMD ["uvicorn", "myfastapi.main:app", "--host", "0.0.0.0", "--port", "80"]