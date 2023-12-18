FROM python:3.12

RUN pip install -- upgrade pip

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app

COOPY ./entrypoint.sh .
ENTRYPOINT ["sh", "/app/entrypoint.sh"]