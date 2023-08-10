FROM ubuntu:20.04

ENV TZ=Europe/Moscow DEBIAN_FRONTEND=noninteractive

RUN mkdir -p /var/log/myapp && chown nobody:nogroup /var/log/myapp

RUN ln -sf /dev/stdout /var/log/myapp/stdout.log \
    && ln -sf /dev/stderr /var/log/myapp/stderr.log

RUN apt-get update && apt-get install -y python3 python3-pip

RUN apt-get install -y --no-install-recommends  ffmpeg

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

CMD ["python3", "run.py"]
