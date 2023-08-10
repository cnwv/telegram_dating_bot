FROM ubuntu:20.04

ENV TZ=Europe/Moscow DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y python3 python3-pip

RUN apt-get install -y --no-install-recommends  ffmpeg

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

# Create symbolic links for logs
RUN ln -sf /dev/stdout /var/log/app-logs/access.log \
    && ln -sf /dev/stderr /var/log/app-logs/error.log \

CMD ["python3", "run.py"]
