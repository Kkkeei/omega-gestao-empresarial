# ÔMEGA — Plataforma de Gestão Empresarial

V2 criada a partir dos documentos de requisitos e da base real `dados/CADASTRO.xlsx`.

## Subir backend com Uvicorn

```bash
cd backend
source /run/media/davi/PROJETOS/meu_venv/bin/activate
pip install -r requirements.txt
# confirme o DATABASE_URL no .env
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Swagger: http://localhost:8000/docs
Health: http://localhost:8000/health

## Importar as empresas da CADASTRO.xlsx

Com o PostgreSQL e o banco `omega` criados:

```bash
cd backend
python scripts/importar_cadastro.py
```

O importador usa o CNPJ como chave, não duplica registros e marca a origem como `IMPORTACAO_CADASTRO`.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

O frontend usa `VITE_API_URL` e, por padrão, aponta para `http://localhost:8000/api/v1`.

## Desenvolvimento local — SQLite

Esta versão usa SQLite por simplicidade no desenvolvimento e na apresentação. Não é necessário instalar PostgreSQL.

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Banco criado automaticamente em `backend/omega.db`.

### Importar CADASTRO.xlsx

Com o backend instalado:

```bash
cd backend
python scripts/importar_cadastro.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

O frontend usa os dados de demonstração enquanto a integração com a API não estiver conectada.

## Certidão Estadual — SEFAZ-PE

A Plataforma ÔMEGA agora possui integração do módulo de Certidões com a Certidão de Regularidade Fiscal da SEFAZ Pernambuco/e-Fisco.

Fluxo: Empresa → Certidões → Certidão Estadual → Consultar → Playwright/e-Fisco → PDF → análise → banco/histórico → visualização.

No backend, instale as dependências com `pip install -r backend/requirements.txt` e o navegador com `playwright install chromium`.

## Persistência permanente de certidões

O módulo de certidões mantém um histórico fiscal permanente e append-only. Cada consulta gera um registro em `consultas_certidoes` e um snapshot imutável em `certidoes_historico`. PDFs são armazenados com nome único e hash SHA-256, sem sobrescrever versões anteriores.

A base SQLite usa WAL + `synchronous=FULL` e, após cada consulta registrada, o sistema cria uma cópia consistente e não sobrescrita em `storage/backups/database/AAAA/MM/`. Consultas, snapshots e documentos de certidão não podem ser apagados por SQL; a exclusão de uma empresa que possua histórico de certidões também é bloqueada.
