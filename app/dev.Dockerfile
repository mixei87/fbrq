FROM python:3.12.1-slim-bullseye
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install -y netcat-traditional

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY entrypoint_web.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint_web.sh
RUN chmod +x /usr/src/app/entrypoint_web.sh

COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint_web.sh"]