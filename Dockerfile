FROM python:3.10-bookworm

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src/* ./

CMD ["python", "bot.py"]
