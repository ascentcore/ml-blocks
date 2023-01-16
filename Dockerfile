FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

WORKDIR /app/

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./logging.conf /app/logging.conf

COPY . /app

ENV PYTHONPATH=/app

RUN apt-get update

# RUN apt-get install ffmpeg libsm6 libxext6  -y

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload", "--reload-delay 1" ]