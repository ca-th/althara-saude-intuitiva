# Conteúdo final e correto para o arquivo: Frontend/Dockerfile

# --- Estágio 1: Build (Onde a "mágica" do Angular acontece) ---
# Usamos uma imagem completa do Node.js para ter as ferramentas de compilação
FROM node:20 AS build

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de definição de pacotes
COPY package*.json ./

# Instala as dependências do npm
RUN npm install

# Copia todo o resto do código do seu projeto Angular
COPY . .

# Compila a aplicação para produção. Isso gera uma pasta 'dist/' com os arquivos finais.
RUN npm run build


# --- Estágio 2: Serve (Onde o site fica no ar) ---
# Usamos uma imagem super leve de um servidor web (Nginx) para servir os arquivos
FROM nginx:alpine

# Copia os arquivos compilados do estágio anterior para a pasta do Nginx
# ATENÇÃO: Verifique se o caminho 'dist/althara-saude-intuitiva' está correto,
# conforme o seu arquivo 'angular.json'
COPY --from=build /app/dist/althara-saude-intuitiva/browser /usr/share/nginx/html

# Expõe a porta 80, que é a porta padrão do Nginx
EXPOSE 80
