FROM python:3.7 AS builder

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.7-slim

ARG APP_PATH=/animon/processing

WORKDIR $APP_PATH

COPY --from=builder /root/.local /root/.local
COPY . $APP_PATH

WORKDIR $APP_PATH
ENTRYPOINT $APP_PATH/entrypoint.sh

