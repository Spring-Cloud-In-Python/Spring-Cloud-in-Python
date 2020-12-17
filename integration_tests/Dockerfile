FROM python:3.7
RUN mkdir /app
COPY . /app
WORKDIR /app
EXPOSE 80
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
