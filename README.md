# Tradutor de Técniques - API Rest

Esta API utiliza FastAPI e IA (Google Gemini) para traduzir pedidos de funcionalidades descritas em linguagem natural por usuários leigos para especificações técnicas estruturadas, e em seguida, estima a complexidade desse desenvolvimento.

## Funcionalidades

1.  **Quebrar Tarefas (`POST /projeto/QuebrarTarefas`)**: Recebe um pedido simples (ex: "Criar tela de login com Google") e retorna as subtarefas técnicas (Frontend, Backend, Database).
2.  **Estimar Complexidade (`POST /tarefa/EstimarComplexidade`)**: Recebe a lista de tarefas técnicas e retorna uma estimativa de complexidade, horas, riscos e sugestões para facilitar o desenvolvimento.

## Como rodar o projeto localmente

### 1. Pré-requisitos
- Python 3.9+ instalado no sistema.
- Chave de API do Google Gemini. Obtenha uma no [Google AI Studio](https://aistudio.google.com/).

### 2. Configurar o Ambiente

No terminal, navegue até a pasta do projeto (`D:\Pós IA\Atividades\Atividade API`):

```bash
# Criar a virtual environment (venv)
python -m venv venv

# Ativar a virtual environment (no Windows PowerShell)
.\venv\Scripts\Activate.ps1
# Ou se for no Command Prompt:
.\venv\Scripts\activate.bat

# Instalar dependências
pip install -r requirements.txt
```

### 3. Configurar a Chave de API

1. Copie o arquivo `.env.example` e renomeie a cópia para `.env`
2. Abra o `.env` e cole a sua chave do Gemini no lugar de `COLOQUE_SUA_CHAVE_AQUI`.

### 4. Iniciar o Servidor

Com a `venv` ativada, rode o comando:
```bash
uvicorn main:app --reload
```

A API estará rodando em `http://127.0.0.1:8000`.

### 5. Como Testar

Acesse a documentação interativa (Swagger UI) gerada automaticamente pelo FastAPI no seu navegador:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Por lá, você pode enviar as requisições para os 2 endpoints e ver os resultados em JSON gerados pela Inteligência Artificial.
