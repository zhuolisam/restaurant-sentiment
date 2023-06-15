FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

RUN apt-get -y update && apt-get install -y --no-install-recommends build-essential  \
    && pip install --upgrade pip setuptools \ 
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY /app .

RUN pip install -r requirements.txt

EXPOSE 8000

# Start app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]