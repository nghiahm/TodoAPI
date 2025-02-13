FROM python:3.13.2-slim-bookworm AS python

ENV POETRY_VERSION=2.0.1
ENV POETRY_HOME=/opt/poetry
ENV PYSETUP_PATH=/opt/pysetup
ENV VENV_PATH=/opt/pysetup/.venv

# Prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

FROM python AS python-build-stage

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
    # dependencies for building Python packages
    build-essential \
    # psycopg dependencies
    libpq-dev \
    # dependencies for installing poetry
    curl

# Install poetry with POETRY_VERSION & POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy pyproject.toml
WORKDIR $PYSETUP_PATH
COPY TodoAPI/pyproject.toml TodoAPI/poetry.lock ./

# Install dependencies using poetry
RUN poetry config virtualenvs.in-project true \
    && poetry install --no-interaction --no-ansi --no-root

FROM python AS python-run-stage

ARG APP_HOME=/app

# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    # psycopg dependencies
    libpq-dev  \
    wait-for-it \
    # Translations dependencies
    gettext \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Copy in our built poetry and venv
COPY --from=python-build-stage $POETRY_HOME $POETRY_HOME
COPY --from=python-build-stage $PYSETUP_PATH $PYSETUP_PATH

# Install as run stage dependencies are already installed
WORKDIR $PYSETUP_PATH
RUN poetry install --no-root

WORKDIR $APP_HOME

COPY /TodoAPI $APP_HOME

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
