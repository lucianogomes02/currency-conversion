FROM python:3.12

RUN pip install --upgrade pip
RUN pip install poetry
ENV PATH="${PATH}:/root/.poetry/bin"

WORKDIR /usr/src/app
COPY . .

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root

EXPOSE 8000

CMD [ "fastapi", "run", "application/main.py"]