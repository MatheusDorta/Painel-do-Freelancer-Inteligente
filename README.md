# 🤖 Painel do Freelancer Inteligente

![Status](https://img.shields.io/badge/status-concluído-brightgreen)

Um Micro-SaaS Full-Stack que automatiza a prospecção de projetos de freelancer, notificando o usuário em tempo real sobre novas oportunidades.

_Coloque aqui um screenshot do seu dashboard funcionando!_

---

## 🎯 Sobre o Projeto

Este projeto foi construído para resolver um problema comum para freelancers: a necessidade de verificar constantemente múltiplas plataformas em busca de novos projetos. O Painel do Freelancer Inteligente automatiza esse processo, funcionando como um assistente pessoal que busca, filtra e notifica sobre novas vagas, permitindo que o usuário foque no que realmente importa: trabalhar nos projetos.

A aplicação foi desenvolvida como um projeto full-stack completo, demonstrando habilidades em Backend, Engenharia de Dados, Frontend e automação.

## ✨ Principais Funcionalidades

* **Scraper Automatizado:** Um robô em Python (`Requests` + `BeautifulSoup`) que varre sites de freelancers em busca de novos projetos.
* **API Robusta:** Um backend em `FastAPI` que gerencia toda a lógica, dados e autenticação.
* **Banco de Dados:** Persistência de dados de usuários e projetos com `SQLAlchemy` e `SQLite`.
* **Autenticação Segura:** Sistema de registro e login com hashing de senhas (`Passlib`) e tokens de acesso `JWT`.
* **Dashboard Interativo:** Uma interface de usuário em `HTML`, `CSS` e `JavaScript` onde o usuário pode visualizar os projetos encontrados.
* **Agendamento de Tarefas:** O robô é executado automaticamente em intervalos de tempo definidos com `APScheduler`.
* **Notificações em Tempo Real:** Alertas instantâneos sobre novos projetos enviados via um bot do **Telegram**.

---

## 🏗️ Arquitetura do Sistema

```
+------------------+      +-----------------------+      +---------------------+
|                  |      |                       |      |                     |
|  Sites de Freela |----->|  Robô "Caçador" (Py)  |----->|  Banco de Dados     |
|  (99Freelas, etc)|      |   (Roda via Scheduler)|      |   (Usuários, Projs) |
|                  |      |                       |      |                     |
+------------------+      +-----------------------+      +----------+----------+
                                                                    ^
                                                                    | (Lê e Escreve)
                                                                    v
+------------------+      +-----------------------+      +----------+----------+
|                  |      |                       |      |                     |
|  Usuário         |----->| Painel Web (HTML/CSS/JS)|<---->|   API Central (Py)  |
|  (Navegador)     |      |   (Faz login, vê projs) |      |      (FastAPI)      |
|                  |      |                       |      |                     |
+------------------+      +-----------------------+      +----------+----------+
                                                                    |
                                                                    | (Envia Alerta)
                                                                    v
                                                         +----------+----------+
                                                         |                     |
                                                         |  Notificador        |
                                                         |  (API do Telegram)  |
                                                         |                     |
                                                         +---------------------+
```

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python, FastAPI, Uvicorn
* **Banco de Dados:** SQLAlchemy, SQLite
* **Web Scraping:** Requests, BeautifulSoup4
* **Segurança:** Passlib, Bcrypt, python-jose (JWT)
* **Automação:** APScheduler
* **Notificação:** python-telegram-bot
* **Frontend:** HTML5, CSS3, JavaScript
* **Variáveis de Ambiente:** python-dotenv

---

## 🚀 Como Começar

Siga os passos abaixo para executar o projeto localmente.

### Pré-requisitos

* Python 3.8+ instalado.
* Uma conta no Telegram.

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git](https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git)
    cd NOME_DO_REPOSITORIO
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Cria o ambiente
    python -m venv .venv

    # Ativa no Windows (PowerShell)
    .\.venv\Scripts\Activate.ps1

    # Ativa no Linux/macOS
    source .venv/bin/activate
    ```

3.  **Crie seu arquivo de ambiente:**
    * Crie um arquivo chamado `.env` na raiz do projeto.
    * Pegue seu Token e Chat ID do Telegram, como explicado no projeto.
    * Adicione-os ao arquivo `.env`:
        ```
        TELEGRAM_BOT_TOKEN="SEU_TOKEN_AQUI"
        TELEGRAM_CHAT_ID="SEU_CHAT_ID_AQUI"
        ```

4.  **Instale as dependências:**
    * Certifique-se de que você tem um arquivo `requirements.txt`. Se não tiver, crie-o com:
        ```bash
        pip freeze > requirements.txt
        ```
    * Instale todas as bibliotecas:
        ```bash
        pip install -r requirements.txt
        ```

5.  **Execute a aplicação:**
    ```bash
    uvicorn main:app --reload
    ```
    A API estará rodando em `http://127.0.0.1:8000`.

---

## 📖 Como Usar

1.  Acesse `http://127.0.0.1:8000` no seu navegador.
2.  Como é o primeiro uso, crie uma conta. Vá para a documentação da API em `http://127.0.0.1:8000/docs`, encontre o endpoint `POST /usuarios/` e crie seu usuário.
3.  Volte para a página de login e entre com suas credenciais.
4.  O robô rodará automaticamente em segundo plano a cada 5 minutos (configurável no `main.py`). Quando ele encontrar um novo projeto, você será notificado no Telegram e o projeto aparecerá no seu dashboard.

---
## 🌟 Autor

Feito com ❤️ por **Matheus Dorta do Nascimento**.