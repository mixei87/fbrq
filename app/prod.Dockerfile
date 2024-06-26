###########
# BUILDER #
###########

FROM python:3.12.1-slim-bullseye as builder
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install -y --no-install-recommends gcc

RUN pip install --upgrade pip
RUN pip install flake8==7.0.0
COPY . /usr/src/app/
RUN flake8 --ignore=E501,F401 .

COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

FROM python:3.12.1-slim-bullseye

RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
#RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

RUN apt update && apt install -y --no-install-recommends netcat-traditional
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

COPY entrypoint_web.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME/entrypoint.sh

COPY . $APP_HOME

RUN chown -R app:app $APP_HOME

USER app

ENTRYPOINT ["sh", "/home/app/web/entrypoint.sh"]