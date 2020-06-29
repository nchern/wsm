FROM python:3.5-alpine 

RUN apk add gcc build-base postgresql-dev

ENV APP_DIR /wsm

ADD  . $APP_DIR

WORKDIR $APP_DIR

RUN make deps

RUN make test

ENTRYPOINT ["./wsm.py"]
