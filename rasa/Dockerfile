FROM rasa/rasa:latest


USER root

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER 1001
