FROM python:2.7-alpine

COPY app/ /app

RUN /bin/sh -c 'cd /app; \
pip install -r requirements.txt'

CMD ["python", "/app/app.py"]