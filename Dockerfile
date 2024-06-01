FROM python:3.12.1-slim-bookworm as python-base
LABEL maintainer = "Maxfield Chen"
LABEL description = "Frame Hello world time keeper"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
ENV HOST_PATH="./host"


# Poetry install stage
FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends --assume-yes \
    curl \
    build-essential 

RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python3 -

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

RUN --mount=type=cache,target=/root/.cache \
    poetry install --without=dev

# test image
FROM python-base as development
WORKDIR $PYSETUP_PATH

COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

RUN --mount=type=cache,target=/root/.cache \
    poetry install --with=dev

COPY ./domain /app/domain/
COPY ./tests /app/tests/
COPY main.py /app/main.py
COPY ./.env /app/.env
COPY ./creds /app/creds
WORKDIR /app
ENTRYPOINT ["python", "-m", "pytest", "tests", "-v", "--tb=short"]

# production image
FROM python-base as production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY ./domain /app/domain
COPY main.py /app/main.py
COPY ./.env /app/.env
COPY ./creds /app/creds
WORKDIR /app

CMD ["bash", "startup.sh"]