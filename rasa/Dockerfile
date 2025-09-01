# Conteúdo final e corrigido para o arquivo: rasa/Dockerfile

FROM rasa/rasa:latest

# Trocamos para o usuário root temporariamente para ter permissão total
USER root

# Atualizamos o pip para a versão mais recente
RUN pip install --upgrade pip

# Copiamos o arquivo de dependências primeiro
COPY requirements.txt .

# Rodamos a instalação de dependências como root
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos o resto do projeto
COPY . .

# Voltamos para o usuário padrão e seguro do Rasa
USER 1001

# O CMD (comando para rodar) é herdado da imagem base, não precisamos definir