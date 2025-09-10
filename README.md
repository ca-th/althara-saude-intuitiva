# Sistema de Agendamento Médico com Chatbot Inteligente
Oi, pessoal! 👋

Queria compartilhar um projeto muito especial para mim. Tudo começou como um trabalho para a faculdade, mas eu gostei tanto do desafio que decidi aprofundar-me e transformá-lo num sistema completo por conta própria. O resultado é este assistente virtual inteligente que ajuda pacientes a agendarem consultas médicas.

A maior aventura foi, sem dúvida, construir tudo com uma **arquitetura de microsserviços**, onde cada parte do sistema (o site, o "cérebro" da IA, a base de dados) funciona de forma independente dentro de contentores **Docker**. Foi uma jornada de muita aprendizagem!

## O que o projeto faz de legal?

* **Um Ambiente Completo no Docker:** A parte que mais gostei foi fazer tudo funcionar junto com o Docker. O frontend, o backend, a IA, a base de dados... tudo sobe com um único comando!
* **Análise de Sintomas com IA Generativa:** Integrei a **API do Google Gemini** para uma funcionalidade que achei incrível: o paciente pode descrever os seus sintomas e o bot recomenda a especialidade médica mais adequada.
* **Conversa Fluida para Agendar:** Usei o **Rasa** para construir o fluxo da conversa. O objetivo era que o agendamento fosse o mais natural possível, como conversar com uma pessoa.
* **Tudo Conectado:** O agendamento feito no chat é guardado em tempo real num banco de dados **MySQL**, o que significa que o sistema funciona de ponta a ponta.
* **Interface Moderna:** O site (frontend) foi feito em **Angular** para ser rápido e fácil de usar.

## As Tecnologias que Usei

* **🐳 Orquestração:** Docker & Docker Compose
* **🤖 IA Conversacional:** Rasa
* **✨ IA Generativa:** Google Gemini API
* **⚙️ Backend:** Python com FastAPI
* **🖥️ Frontend:** Angular
* **🗃️ Banco de Dados:** MySQL

## Como Tudo "Conversa"? A Arquitetura

O sistema é um ecossistema com 6 serviços a comunicarem entre si:

1.  **`frontend`**: O site em Angular que o usuário vê.
2.  **`backend`**: É uma API em FastAPI que recebe os pedidos do site e os distribui para os outros serviços.
3.  **`rasa`**: O "cérebro" principal do chatbot, que entende o que o usuário quer dizer.
4.  **`rasa-actions`**:  É aqui que o código Python se conecta com a API do Gemini e com o banco de dados para fazer as coisas a sério.
5.  **`db`**: O banco de dados MySQL, que guarda tudo de forma segura.
6.  **`duckling`**: Um ajudante do Rasa que é ótimo a perceber datas e horas no meio da conversa.

## Quer Testar na Sua Máquina?

Com o Docker, é super simples!

**O que você vai precisar:**

* Docker e Docker Compose instalados.
* Git.

**Passos:**

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/ca-th/althara-saude-intuitiva.git](https://github.com/ca-th/althara-saude-intuitiva.git)
    cd nome-do-repositorio
    ```

2.  **Configure as suas chaves:**
    * Abra o ficheiro `.env` que está na raiz do projeto.
    * Coloque as suas senhas para o banco de dados e a sua chave da API do Google Gemini nos campos correspondentes.

3.  **Suba tudo!**
    * Este é o único comando que você precisa. Ele vai construir e iniciar todos os 6 serviços de uma vez.
    ```bash
    docker-compose up --build
    ```

4.  **Aceda à Aplicação:**
    * Aguarde alguns minutos para que todos os serviços, especialmente o Rasa, carreguem os modelos de IA.
    * Abra o seu navegador e aceda a `http://localhost:4200`.

E pronto! O sistema completo estará a funcionar. Espero que gostem!

