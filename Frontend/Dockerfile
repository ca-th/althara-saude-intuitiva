FROM node:20 AS build


WORKDIR /app


COPY package*.json ./


RUN npm install

COPY . .


RUN npm run build


# imagem super leve de um servidor web (Nginx) para servir os arquivos
FROM nginx:alpine


COPY --from=build /app/dist/althara-saude-intuitiva/browser /usr/share/nginx/html

#  é a porta padrão do Nginx
EXPOSE 80
