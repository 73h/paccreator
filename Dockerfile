FROM python:3.11

RUN useradd --create-home --home /code pyapp
USER pyapp
WORKDIR /code

ENV VIRTUAL_ENV=/code/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY --chown=app pyproject.toml requirements.txt ./
RUN mkdir src
RUN pip install --editable .[test]

COPY --chown=pyapp . .
