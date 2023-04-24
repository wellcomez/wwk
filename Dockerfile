FROM python:3.6

# MAINTAINER Mr Gao
COPY  WanKeYunApi/* /app/WanKeYunApi/
COPY *.py /app/
COPY index.html /app/
COPY onethingcloud/*.py /app/onethingcloud/
COPY config.ini.blank /app/conf/config.ini
COPY requirements.txt /app/

WORKDIR /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "/app/server.py"]
