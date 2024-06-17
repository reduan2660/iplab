FROM python:3.8-slim

ENV DEPLOYMENT_ENV "dev"
ENV EXPOSE_PORT 8000
ENV GUNICORN_WORKERS 2

RUN apt-get update && apt-get install libpq-dev gcc -y
WORKDIR /project

COPY requirements.txt /project/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY wait-for-it.sh /project/
RUN chmod +x wait-for-it.sh

COPY run.sh /project/
RUN chmod +x run.sh

COPY alembic.ini /project/
COPY app /project/app

EXPOSE 8000
CMD [ "/project/run.sh" ]