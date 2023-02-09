FROM python:3.11.1-buster

LABEL maintainer="JaeHyunL swaa23@gmail.com"
RUN pip install --upgrade pip
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--reload", "--host=0.0.0.0"]