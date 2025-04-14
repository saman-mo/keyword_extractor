FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8


COPY ./app /app/app/

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y \
    python3 python3-pip

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]