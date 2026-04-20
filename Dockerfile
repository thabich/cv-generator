FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y libpango-1.0-0 libpangoft2-1.0-0 libffi-dev libcairo2 \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y libpango-1.0-0 libpangoft2-1.0-0 libffi-dev libcairo2 \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pybabel compile -d translations
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
