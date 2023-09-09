FROM python:3.11

RUN mkdir /app
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .

CMD ["gunicorn", "main:APP", "--bind", "0.0.0.0:80"]
