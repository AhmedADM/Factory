FROM python:3.10

WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt --upgrade
COPY . .

RUN sed -i 's/db_host.*/db_host = db/g' app.conf
RUN sed -i 's/db_port.*/db_port = 5432/g' app.conf

ENTRYPOINT  ["python", "factory_start.py"]