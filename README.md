# 💱 Currency Conversion API

Uma aplicação FastAPI que realiza conversões de moedas, armazenando o histórico por usuário e integrando com um cliente de taxa de câmbio externa.

---

## 📁 Estrutura do Projeto

````
currency-conversion/
│
├── application/ # Configurações principais da aplicação
│ ├── migrations/ # Arquivos de migração do banco de dados (alembic)
│ │ ├── env.py
│ │ └── ...
│ ├── database.py # Configuração do SQLAlchemy + conexão
│ └── main.py # Ponto de entrada da aplicação FastAPI
│
├── infra/ # Código de infraestrutura
│ └── init.py
│
├── libs/ # Código reutilizável e genérico
│ └── repository.py # Repositório genérico para persistência
│
├── src/ # Código da aplicação em si (domínio)
│ ├── models/ # Modelos SQLAlchemy
│ │ └── currency_conversion.py
│ ├── repository/ # Repositórios específicos
│ │ └── currency_conversion.py
│ ├── routers/ # Rotas da API
│ │ └── currency_conversion.py
│ ├── schemas/ # Schemas Pydantic (request/response)
│ │ └── currency_conversion.py
│ ├── services/ # Lógica de negócio (casos de uso)
│ │ ├── currency_conversion.py
│ │ └── exchange_rate_client.py
│ └── tests/ # Testes automatizados
│ └── init.py
│
├── .env # Variáveis de ambiente (local)
├── alembic.ini # Configuração do Alembic
├── conversions.db # Banco SQLite local (pode ser ignorado em produção)
├── poetry.lock / pyproject.toml # Gerenciamento de dependências
└── README.md # Este arquivo
````

---

## ⚙️ Tecnologias Utilizadas

- **FastAPI** – Web framework moderno e rápido
- **SQLAlchemy** – ORM para banco de dados
- **SQLite** – Banco de dados local
- **Alembic** – Migrações de banco de dados
- **Pydantic** – Validação de dados
- **Poetry** – Gerenciador de dependências
- **httpx** – Cliente HTTP para consumo de APIs externas

---

## ▶️ Como Rodar o Projeto

### 1. Clonar o Repositório

```bash
git clone https://github.com/lucianogomes02/currency-conversion.git
cd currency-conversion
```

### 2. Instalar Dependências

```bash
poetry install
poetry shell
```

### 3. Configurar Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
DATABASE_URL=sqlite:///./conversions.db
EXCHANGE_API_BASE_URL=http://api.exchangeratesapi.io/latest
EXCHANGE_RATE_API_KEY=your_api_key_here
```

### 4. Executar Migrações

```bash
alembic upgrade head
```

### 5. Rodar a Aplicação

```bash
uvicorn application.main:app --reload #  Produção (não recomendado para desenvolvimento)
fastapi dev application/main.py # Desenvolvimento
```

### 6. Acessar a API e Documentação
Acesse a documentação interativa da API em:

```
http://localhost:8000/docs
```

### 🏗️ Arquitetura

O projeto segue uma separação em camadas:

```routers```: controladores e endpoints

```schemas```: validação e serialização com Pydantic

```services```: lógica de negócio e orquestração

```repository```: abstração da camada de persistência

```models```: modelos do banco com SQLAlchemy