FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p static/uploads

EXPOSE 5000

ENV FLASK_ENV=development

CMD ["python", "app.py"]