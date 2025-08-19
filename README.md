# Sistema de Agendamento Médico com Chatbot Inteligente

## Visão Geral do Projeto

Este é um sistema completo de agendamento de consultas médicas, projetado para otimizar o fluxo de trabalho de clínicas e profissionais de saúde. O diferencial do projeto é pela integração de um **chatbot inteligente**, que automatiza a interação inicial com o paciente e facilita o processo de agendamento de forma intuitiva.

## Principais Funcionalidades

* **Gerenciamento de Consultas**: Agendamento, alteração e cancelamento de atendimentos.
* **Controle de Especialidades e Profissionais**: Cadastro e gestão de médicos e suas respectivas especialidades.
* **Chatbot Integrado**: Interface conversacional para agendamento de consultas usando processamento de linguagem natural.
* **Interface de Usuário (Frontend)**: Telas responsivas para pacientes e administradores, com visualização de agendamentos e interações com o chatbot.

## Tecnologias Utilizadas

Este projeto foi construído utilizando as seguintes tecnologias:

* **Backend**: Python, com o framework **FastAPI** para criação da API REST.
* **Chatbot**: **Rasa** para gerenciamento de diálogos e processamento de linguagem natural.
* **Banco de Dados**: **MySQL** para armazenamento de dados de usuários, médicos, especialidades e agendamentos.
* **Frontend**: **Angular** para a construção da interface de usuário, garantindo uma experiência dinâmica e responsiva.

## Estrutura e Arquitetura do Sistema

O projeto é dividido em quatro componentes principais, que se comunicam através de requisições HTTP e do banco de dados.

### 1. Backend e API (Python com FastAPI)

Responsável pela lógica de negócios e pela exposição dos dados.
* Gerencia o CRUD (Create, Read, Update, Delete) de atendimentos, especialidades e médicos.
* Valida e processa as requisições vindas tanto do Frontend quanto do chatbot.

### 2. Chatbot (Rasa)

* **Fluxo de Diálogo**: Configurado para entender a intenção do usuário (ex: "quero agendar uma consulta") e guiar a conversa.
* **Processamento de Linguagem Natural**: Analisa as mensagens do paciente para extrair informações relevantes (ex: data, horário, especialidade).
* **Integração**: Conecta-se com a API do Backend para executar ações como verificar a disponibilidade de um médico ou confirmar um agendamento.

### 3. Frontend (Angular)

* **Design Responsivo**: Garante que a aplicação funcione em diferentes dispositivos.
* **Telas de Agendamento**: Interface intuitiva para que pacientes e administradores possam visualizar, criar e gerenciar agendamentos.
* **Interface de Chat**: Componente interativo que se comunica com o chatbot Rasa para permitir a conversa em tempo real.

### 4. Banco de Dados (MySQL)

Armazena todas as informações críticas do sistema, incluindo:
* Tabelas para **usuários, médicos e pacientes**.
* Registros de **especialidades médicas**.
* Histórico e detalhes de **atendimentos e agendamentos**.

## Como Iniciar o Projeto

Para rodar este projeto localmente, siga os seguintes passos para cada componente:

**Pré-requisitos:**
* Python 3.10
* Node.js e npm
* MySQL Server
* Git

**1. Configurar o Banco de Dados MySQL**
* Crie um banco de dados com o nome de sua preferência (por exemplo, `althara_saude`).
* Execute o script de modelagem de dados que está na pasta `SQL/`.

**2. Configurar o Backend**
* Vá para a pasta `Backend/`.
* Crie e ative um ambiente virtual:
    `python -m venv venv`
    `venv\Scripts\activate` (Windows) ou `source venv/bin/activate` (macOS/Linux)
* Instale as dependências:
    `pip install -r requirements.txt`
* Inicie o servidor da API:
    `uvicorn main:app --reload`

**3. Configurar o Chatbot (Rasa)**
* Vá para a pasta `rasa/`.
* Instale o Rasa e as dependências:
    `pip install rasa`
* Treine o modelo do chatbot:
    `rasa train`
* Inicie o servidor do Rasa:
    `rasa run -m models --enable-api --cors "*"`

**4. Configurar o Frontend (Angular)**
* Vá para a pasta `Frontend/`.
* Instale as dependências do Angular:
    `npm install`
* Inicie o servidor de desenvolvimento:
    `ng serve`

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma *issue* para reportar bugs ou uma *pull request* com novas funcionalidades.
