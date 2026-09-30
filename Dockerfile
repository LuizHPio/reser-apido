FROM python:3.12-slim

WORKDIR /bmeta

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python -m app.controllers.db.init_db

EXPOSE 3000

CMD ["python3", "route.py"]