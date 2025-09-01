FROM python:3.10-slim

# --- ADICIONADO: Atualiza os pacotes do sistema operacional base ---
RUN apt-get update && apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# --- ADICIONADO: Atualiza o pip antes de instalar as dependências ---
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]