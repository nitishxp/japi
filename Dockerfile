FROM python:3
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt
COPY . /code/
WORKDIR /code/
COPY ./entrypoint-scripts/web-entrypoint.sh /web-entrypoint.sh
RUN chmod +x /web-entrypoint.sh