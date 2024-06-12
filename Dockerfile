FROM python:3.9-slim as builder

WORKDIR /code

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

COPY ./requirements.txt /code/requirements.txt

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /code/wheels -r /code/requirements.txt

FROM python:3.9-slim

ENV PYTHONPATH /code

WORKDIR /code

COPY --from=builder /code/wheels /wheels
COPY --from=builder /code/requirements.txt .

RUN pip install --no-cache /wheels/*

COPY ./app /code/app

CMD ["fastapi", "run", "./app/main.py", "--port", "4200"]