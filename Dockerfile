FROM tiangolo/uvicorn-gunicorn:python3.9

RUN mkdir ./app
WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN pip install poetry
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi
RUN poetry shell

COPY ./ .

ENV MODULE_NAME "api.app"
ENV WORKERS_PER_CORE 4
