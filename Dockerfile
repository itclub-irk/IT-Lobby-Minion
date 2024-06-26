FROM python:3.12
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
COPY src ./src
COPY db_data ./db_data
COPY logs ./logs
COPY run.py .
CMD ["python3", "run.py"]