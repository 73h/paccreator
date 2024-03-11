FROM python:3.11

COPY pyproject.toml requirements.txt README.md LICENSE ./
COPY ./src /src

RUN pip install --no-cache-dir --editable .[test]

WORKDIR /src/

ENV PYTHONPATH=/src
