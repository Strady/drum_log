# first stage
FROM python:3.9-slim as builder
MAINTAINER Andrew Abramenko (a.i.abramenko@yandex.ru)
ADD . /app
WORKDIR /app
# Compile python dependencies as wheels into specialized folder
RUN mkdir /wheels && pip3 install --upgrade pip setuptools wheel && pip3 wheel . --wheel-dir=/wheels


# second stage
FROM python:3.9-slim
COPY --from=builder /wheels /wheels
ADD . /app
WORKDIR /app
RUN pip3 install --no-index --find-links=/wheels .


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
