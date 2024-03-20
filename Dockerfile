FROM python:latest

COPY setup.py /app/setup.py
COPY godaddydnsupdater /app/godaddydnsupdater
WORKDIR /app

RUN pip install .
CMD ["python3", "godaddydnsupdater"]